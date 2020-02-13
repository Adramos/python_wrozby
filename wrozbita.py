# -*- coding: utf-8 -*-
import random
import datetime
from flask import Flask, escape, request, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime, date


app = Flask(__name__)
app.config['SECRET_KEY'] = '(a+b)^2=a^2+2ab+b^2'


class WrozbaForm(FlaskForm):
    name = StringField(u'Imie',
                       validators=[DataRequired(), Length(min=3, max=20)])
    surname = StringField(u'Nazwisko',
                          validators=[DataRequired(), Length(min=3, max=20)])
    date = DateField(u'Data urodzenia (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField(u'Poznaj swój los')


wrozby = [
    {
        'work': u'Wkrótce uda Ci się ostatecznie rozwiązać ów problem, z którym raz za razem się potykasz. ',
        'luck': u'Będzie Ci sprzyjało szczęście.',
        'love': u'Spodziewaj się miłego zaskoczenia w życiu osobistym.',
        'scary': u'Nie ufaj facetowi z skórzanej kurtce.'
    },
    {
        'work': u'Czarne chmury przysłonią Twoje myśli, będą występowały problemy by skupić się na wykonywanej pracy. Szukaj wtedy ukojenia w muzyce.',
        'luck': u'Czeka Cię seria niepowodzeń. Ale pamiętaj, że na hossa zaczyna się wtedy, gdy już nikt nie wierzy, że może być gorzej.',
        'love': u'Nie kupuj kwiatów, zamiast tego zainwestuj w wyjście na wspólne łyżwy.',
        'scary': u'Lepiej zmień hasło do emaila.'
    }
]



wrozby_work = []
with open('work.txt') as workDivs:
    for wDiv in workDivs:
        wrozby_work.append(wDiv)

wrozby_luck = []
with open('luck.txt') as luckDivs:
    for luDiv in luckDivs:
        wrozby_luck.append(luDiv)

wrozby_love = []
with open('love.txt') as loveDivs:
    for loDiv in loveDivs:
        wrozby_love.append(loDiv)

wrozby_scary = []
with open('scary.txt') as scaryDivs:
    for scDiv in scaryDivs:
        wrozby_scary.append(scDiv)

wrozby_starts = []
with open('starts.txt') as startsDivs:
    for stDiv in startsDivs:
        wrozby_starts.append(stDiv)

#work, luck, love, scary, start1, start2, start3, start4
wrozby_num = []
for i in range(0,8):
    wrozby_num.append(1)


wrozby_stare = [
    {
        'imie': 'test',
        'nazwisko': 'testowy',
        'urodziny': date.today(),
        'wrozby': wrozby_num.copy()
    }
]


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def hello():
    form = WrozbaForm()
    if form.validate_on_submit():

        date_tmp = form.date.data
        date_str = date_tmp.strftime('%Y-%m-%d')
        imie = form.name.data
        nazwisko = form.surname.data

        found = False
        prof = False
        stara_wrozba = wrozby_stare[0]

        if imie == 'Adam' and nazwisko == 'Domański':
            prof = True

        for stare in wrozby_stare:
            if stare['imie'] == imie and stare['nazwisko'] == nazwisko and stare['urodziny'] == date_tmp:
                stara_wrozba = stare.copy()
                found = True
                break

        if (found == True):
            flash(f'Była już jedna wróżba. Oto ona:', 'success')

            wrozby_num[0] = stara_wrozba['wrozby'][0]
            wrozby_num[1] = stara_wrozba['wrozby'][1]
            wrozby_num[2] = stara_wrozba['wrozby'][2]
            wrozby_num[3] = stara_wrozba['wrozby'][3]
            wrozby_num[4] = stara_wrozba['wrozby'][4]
            wrozby_num[5] = stara_wrozba['wrozby'][5]
            wrozby_num[6] = stara_wrozba['wrozby'][6]
            wrozby_num[7] = stara_wrozba['wrozby'][7]
        else:
            flash(f'Oto Twoja wróżba', 'success')
            if prof == False:
                wrozby_num[0] = random.randint(0, len(wrozby_work)-2)
                wrozby_num[1] = random.randint(0, len(wrozby_luck)-2)
                wrozby_num[2] = random.randint(0, len(wrozby_love)-2)
                wrozby_num[3] = random.randint(0, len(wrozby_scary)-2)
            else:
                wrozby_num[0] = len(wrozby_work) - 1
                wrozby_num[1] = len(wrozby_luck) - 1
                wrozby_num[2] = len(wrozby_love) - 1
                wrozby_num[3] = len(wrozby_scary) - 1

            wrozby_num[4] = random.randint(0, len(wrozby_starts)-1)
            wrozby_num[5] = random.randint(0, len(wrozby_starts)-1)
            while wrozby_num[4] == wrozby_num[5]:
                wrozby_num[5] = random.randint(0, len(wrozby_starts)-1)

            wrozby_num[6] = random.randint(0, len(wrozby_starts)-1)
            while wrozby_num[4] == wrozby_num[6] or wrozby_num[5] == wrozby_num[6]:
                wrozby_num[6] = random.randint(0, len(wrozby_starts)-1)

            wrozby_num[7] = random.randint(0, len(wrozby_starts)-1)
            while wrozby_num[4] == wrozby_num[7] or wrozby_num[5] == wrozby_num[7] or wrozby_num[6] == wrozby_num[7]:
                wrozby_num[7] = random.randint(0, len(wrozby_starts)-1)

            nowa_wrozba = {
                'imie': imie,
                'nazwisko': nazwisko,
                'urodziny': date_tmp,
                'wrozby': wrozby_num.copy()
            }
            wrozby_stare.append(nowa_wrozba)
        return redirect(url_for('wrozba', birthsday=date_str, name=imie, surname=nazwisko))

    return render_template('home.html', title = u'Początek', form = form)


@app.route("/wrozba")
def wrozba():

    date_str = request.args['birthsday']
    imie = request.args['name']
    nazwisko = request.args['surname']
    date = datetime.strptime(date_str, '%Y-%m-%d')

    day = date.day
    month = date.month

    if month == 1:
        if day < 20:
            znak_zodiaku = 'Koziorożec'
        else:
            znak_zodiaku = 'Wodnik'
    elif month == 2:
        if day < 19:
            znak_zodiaku = 'Wodnik'
        else:
            znak_zodiaku = 'Ryby'
    elif month == 3:
        if day < 21:
            znak_zodiaku = 'Ryby'
        else:
            znak_zodiaku = 'Baran'
    elif month == 4:
        if day < 20:
            znak_zodiaku = 'Baran'
        else:
            znak_zodiaku = 'Byk'
    elif month == 5:
        if day < 23:
            znak_zodiaku = 'Byk'
        else:
            znak_zodiaku = 'Bliźnięta'
    elif month == 6:
        if day < 22:
            znak_zodiaku = 'Bliźnięta'
        else:
            znak_zodiaku = 'Rak'
    elif month == 7:
        if day < 23:
            znak_zodiaku = 'Rak'
        else:
            znak_zodiaku = 'Lew'
    elif month == 8:
        if day < 24:
            znak_zodiaku = 'Lew'
        else:
            znak_zodiaku = 'Panna'
    elif month == 9:
        if day < 23:
            znak_zodiaku = 'Panna'
        else:
            znak_zodiaku = 'Waga'
    elif month == 10:
        if day < 23:
            znak_zodiaku = 'Waga'
        else:
            znak_zodiaku = 'Skorpion'
    elif month == 11:
        if day < 22:
            znak_zodiaku = 'Skorpion'
        else:
            znak_zodiaku = 'Strzelec'
    else:
        if day < 22:
            znak_zodiaku = 'Strzelec'
        else:
            znak_zodiaku = 'Koziorożec'

    im = imie
    nz = nazwisko
    zn = znak_zodiaku
    return render_template('wrozba.html', title = u'Twoja wróżba', work=wrozby_work, luck=wrozby_luck, love=wrozby_love, scary=wrozby_scary, start=wrozby_starts, number=wrozby_num, imie=im, nazwisko=nz, znak=zn)


if __name__ == '__main__':
    app.run(debug=True)