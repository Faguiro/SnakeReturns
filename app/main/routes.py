from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, send_file
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm
from app.models import User, Post
from app.translate import translate
from app.main import bp
from gtts import gTTS
import time
import random

import os
import sqlite3

import requests
import json
import xml.etree.ElementTree as ET
import re

basedir = os.path.abspath(os.path.dirname(__file__))

texto='Bem vindos!'

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/site', methods=['GET', 'POST'])
def site():
    return render_template('portifolio.html')

@bp.route('/site1', methods=['GET', 'POST'])
def site1():
    return render_template('site1.html')



@bp.route('/fala', methods=['GET', 'POST'])
def fala(texto="Bem vindo!"):
    r1 = random.randint(1,10000000)
    r2 = random.randint(1,10000000)
    randfile = str(r2)+"randomtext"+str(r1) +".mp3"
    tts = gTTS(texto,lang='pt-br')
    time.sleep(2)
    return render_template('fala.html')
    #Teste de uso:
    #texto=input('Texto:')
    #fala(texto)
    # Contato: faguiro2005@gmail.com


@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You are following %(username)s!', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You are not following %(username)s.', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/fala2', methods=['GET', 'POST'])
def fala2():
    return render_template('fala2/index.html')


@bp.route('/info', methods=['GET'])
def info():
    return render_template('info.html')



@bp.route('/getinfo', methods=['GET', 'POST'])
def getinfo():
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    ip="201.19.71.179"
    def check(Ip):
        if(re.search(regex, Ip)):
            return True
        else:
            return False

    if check(ip):
        ip_publico ='201.19.71.179'
    else:
        ip_publico = requests.get('https://api.ipify.org').text
        #ip_publico ='201.19.71.179'
    try:
        #pais = requests.get(f"https://ip2c.org/{ip_publico}").text.split(';')[-1]
        dt = requests.get(f"http://www.geoplugin.net/xml.gp?ip={ip_publico}").text
        root = ET.fromstring(dt)
    except:
        return  requests.get(f"http://www.geoplugin.net/xml.gp?ip={ip_publico}").text

    def _cat(field):
        for x in root.findall(field):
            return x.text

    estado = _cat("geoplugin_regionName")
    cidade = _cat("geoplugin_city")
    latitude = _cat("geoplugin_latitude")
    longitude = _cat("geoplugin_longitude")
    cod_pais = _cat("geoplugin_countryCode")
    moeda = _cat("geoplugin_currencySymbol_UTF8")

    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    s2 = now.strftime("%d/%m/%Y")
    x = {
        "data": s2,
        "hora": t,
        "ip": ip_publico,
        "estado": estado,
        "cidade": cidade,
        "latitude": latitude,
        "longitude": longitude,
        "cod_pais": cod_pais,
        "moeda": moeda
    }

    y = json.dumps(x)
    return y


@bp.route('/pokedex', methods=['GET'])
def pokedex():
    return render_template('pokedex/index.html')


@bp.route('/baralho', methods=['GET'])
def baralho():
    return render_template('baralho/baralho.html')




@bp.route('/pomodoro_app')
def download():
    return send_file('downloads/simple_pomodoro.zip', as_attachment=True)


@bp.route('/png-to-ico')
def download_png_to_ico():
    return send_file('downloads/tk_conversor.exe', as_attachment=True)


def criar_tabela():
    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT,
            latitude TEXT,
            longitude TEXT,
            enderecoIP TEXT,
            startTime TEXT,
            navegador TEXT,
            versaoNavegador TEXT,
            sistemaOperacional TEXT,
            tipoDispositivo TEXT,
            referenciaOrigem TEXT,
            idiomaPreferido TEXT,
            tempoPermanencia REAL
        )
    ''')

    conn.commit()
    conn.close()

def atualizar_ou_adicionar(dados, novo_registro):
    ip = novo_registro['enderecoIP']
    for index, registro in enumerate(dados):
        if registro[index] == ip:
            dados[index] = novo_registro
            return
    dados.append(novo_registro)

@bp.route('/receber-dados', methods=['POST'])
def receber_dados():
    novo_registro = request.json

    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    campos = [
        'name', 'email', 'latitude', 'longitude',
        'enderecoIP', 'startTime', 'navegador', 'versaoNavegador',
        'sistemaOperacional', 'tipoDispositivo', 'referenciaOrigem',
        'idiomaPreferido', 'tempoPermanencia'
    ]

    campos_valores = []
    valores = []

    for campo in campos:
        if campo in novo_registro:
            campos_valores.append(campo)
            valores.append(novo_registro[campo])

    campos_str = ', '.join(campos_valores)
    placeholders = ', '.join(['?' for _ in valores])

    insert_query = f'INSERT INTO registros ({campos_str}) VALUES ({placeholders})'

    cursor.execute(insert_query, tuple(valores))
    conn.commit()
    conn.close()

    return jsonify(message='Dados recebidos e salvos com sucesso')

@bp.route('/teste', methods=['GET'])
@bp.route('/mostrar-dados', methods=['GET'])
def mostrar_dados():
    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()

    conn.close()

    return render_template('tabela_dados.html', registros=registros)

@bp.route('/usuarios-mais-tempo', methods=['GET'])
def usuarios_mais_tempo():
    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    # Seleciona o registro com maior tempo de permanência para cada IP único
    query = '''
        SELECT id, name, email, enderecoIP, MAX(tempoPermanencia)
        FROM registros
        GROUP BY enderecoIP
        ORDER BY MAX(tempoPermanencia) DESC
    '''
    cursor.execute(query)
    usuarios = cursor.fetchall()

    conn.close()

    return render_template('usuarios_mais_tempo.html', usuarios=usuarios)

@bp.route('/quantidade-acessos', methods=['GET'])
def quantidade_acessos():
    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    query = '''
        SELECT strftime('%Y-%m-%d', startTime) as data, enderecoIP, COUNT(*) as quantidade
        FROM registros
        GROUP BY data, enderecoIP
    '''
    cursor.execute(query)
    dados = cursor.fetchall()

    conn.close()

    return render_template('quantidade_acessos.html', dados=dados)

@bp.route('/quantidade-acessos-por-usuario', methods=['GET'])
def quantidade_acessos_por_usuario():
    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    query = '''
        SELECT enderecoIP, COUNT(*) as quantidade
        FROM registros
        GROUP BY enderecoIP
    '''
    cursor.execute(query)
    dados = cursor.fetchall()

    conn.close()

    return render_template('quantidade_acessos_por_usuario.html', dados=dados)

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')



@bp.route('/atualizar-nome-email', methods=['POST'])
def atualizar_nome_email():
    nome = request.form.get('nome')
    email = request.form.get('email')
    endereco_ip = request.form.get('id')
    print(nome, email, endereco_ip)


    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    cursor.execute('UPDATE registros SET name = ?, email = ? WHERE enderecoIP = ?', (nome, email, endereco_ip))
    conn.commit()
    conn.close()

    return jsonify(message='Dados atualizados com sucesso')


@bp.route('/buscar-por-ip', methods=['GET', 'POST'])
def buscar_por_ip():
    if request.method == 'POST':
        endereco_ip = request.form.get('endereco_ip')

        conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
        cursor = conn.cursor()

        query = '''
            SELECT name, email, enderecoIP, latitude, longitude, MAX(tempoPermanencia) AS maior_tempo, COUNT(*) AS quantidade_acessos
            FROM registros
            WHERE enderecoIP = ?
        '''
        cursor.execute(query, (endereco_ip,))
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            nome, email, ip, latitude, longitude, maior_tempo, quantidade_acessos = resultado
            return render_template('buscar_por_ip_resultado.html', nome=nome, email=email, ip=ip, latitude=latitude, longitude=longitude, maior_tempo=maior_tempo, quantidade_acessos=quantidade_acessos)
        else:
            return render_template('buscar_por_ip_resultado.html', mensagem='IP não encontrado')

    return render_template('buscar_por_ip.html')


def atualizar_latitude_longitude_faltando():
    conn = sqlite3.connect(os.path.join(basedir, 'dados.db'))
    cursor = conn.cursor()

    # Seleciona os registros com latitude e longitude faltando
    query = '''
        SELECT enderecoIP
        FROM registros
        WHERE latitude IS NULL OR longitude IS NULL
    '''
    cursor.execute(query)
    ips_com_dados_faltando = cursor.fetchall()

    for ip in ips_com_dados_faltando:
        ip = ip[0]  # Pega o valor do primeiro elemento da tupla (o endereço IP)

        # Seleciona um registro com latitude e longitude preenchidos para o mesmo IP
        query = '''
            SELECT latitude, longitude
            FROM registros
            WHERE enderecoIP = ? AND latitude IS NOT NULL AND longitude IS NOT NULL
            LIMIT 1
        '''
        cursor.execute(query, (ip,))
        registro_com_dados = cursor.fetchone()

        if registro_com_dados:
            latitude, longitude = registro_com_dados
            # Atualiza os registros com latitude e longitude faltando
            query = '''
                UPDATE registros
                SET latitude = ?, longitude = ?
                WHERE enderecoIP = ? AND (latitude IS NULL OR longitude IS NULL)
            '''
            cursor.execute(query, (latitude, longitude, ip))
            conn.commit()

    conn.close()

    print('Atualização concluída com sucesso')




