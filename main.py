"""O objetivo do código é criar um site que mostre uma relação de coffee shops, com uma primeira
 página da apresentação com um botão de link que mostra uma tabela com o nome da loja um link para sua
 localização e mais alguns dados de classificação"""
"""primeiro, importou flask e suas funcionalidades, render_template, para lidar com o html, redirect, que é uma
função do Flask para lidar com o redirecionamento da URL, e o url_for, que, pelo que entendi, é uma facilitador
na criação de rotas, onde se passa o nome da função e ele já cria a rota. Também foi importado o Bootstrap
que já contem vários códigos e templates prontas, o flasform para trabalhar com formulários, 
os campos de preenchimentos de nomes e os validadores, além da csv para lidar com a tabela dos cafés relacionados"""
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

"""aqui, a configuração de inicialização do Flask, a secret key do  CRSF, eu acho, e a inicialização do
Bootstrap"""
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

"""aqui foi criada a classe que contém os elementos que irão compor a tabela das lojas, cada campo
vem com o nome do campo, com o tipo e com os validadores necessários."""


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                              validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


"""aqui o código para a página inicial, que vai renderizar o código do index"""


@app.route("/")
def home():
    return render_template("index.html")


"""aqui a rota que vai desviar para o add, que só pode ser acessado por hard coding, ou seja,
digitando o endereço, e a intenção é acessar um formulário que modifique a tabela dos coffees shops
Abaixo é criada uma função para incluir itens na tabela, form parece que é uma palavra reservada do Flask WTF
para o formulário, já o validate_on_submit serve para quando uma rota aceita o get e o post, mas só se quer
validar um post request. Então será aberta a tabela com o método with open,que abre o arquivo selecionado e 
o  comando a, significa append. O método write vai acessar os dados (data) do formulário (form) no campo que foi
acima criado na class CafeForm. Pelo que entendi, quando se escreve a rota com o /add, ele desvia para esse formulário
e ao se clicar no botão submit, ele volta para a rota /cafes 
"""


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form: CafeForm = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


"""Aqui a rota para /cafes onde é mostrada a tabela da lojas de café. O método with open
abre a tabela como um arquivo csv, método para ler informações em tabelas, acima importado.
Depois é usado o método reader, criada uma tabela vazia que será preenchida pelo for loop abaixo.
Não entendi como a informação vai para a tabela certa, quando abro o arquvo cafe-data.csv ele já está prennchido,
mas o delimitador , está nas classes acima"""


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
