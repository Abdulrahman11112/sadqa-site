from flask import Flask, request, redirect, render_template_string, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sadqa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    subhan = db.Column(db.Integer, default=0)
    hamd = db.Column(db.Integer, default=0)
    akbar = db.Column(db.Integer, default=0)

    @property
    def total(self):
        return self.subhan + self.hamd + self.akbar


home_page = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>صدقة جارية</title>
    <style>
        *{
            box-sizing:border-box;
        }

        body{
            margin:0;
            font-family:Arial, sans-serif;
            background:linear-gradient(135deg,#0f172a,#1e3a8a,#0f766e);
            min-height:100vh;
            color:white;
            display:flex;
            align-items:center;
            justify-content:center;
            padding:20px;
        }

        .container{
            width:100%;
            max-width:520px;
            background:rgba(255,255,255,0.12);
            backdrop-filter:blur(10px);
            border:1px solid rgba(255,255,255,0.15);
            border-radius:24px;
            padding:30px;
            box-shadow:0 20px 60px rgba(0,0,0,0.35);
            text-align:center;
        }

        h1{
            margin-top:0;
            font-size:30px;
            line-height:1.6;
        }

        .subtitle{
            opacity:0.95;
            margin-bottom:24px;
            line-height:1.8;
            font-size:17px;
        }

        .card{
            background:white;
            color:#111827;
            border-radius:18px;
            padding:24px;
        }

        input{
            width:100%;
            padding:14px;
            border-radius:12px;
            border:1px solid #d1d5db;
            font-size:16px;
            margin-bottom:14px;
            outline:none;
        }

        input:focus{
            border-color:#2563eb;
        }

        button{
            width:100%;
            padding:14px;
            border:none;
            border-radius:12px;
            background:#2563eb;
            color:white;
            font-size:17px;
            cursor:pointer;
        }

        button:hover{
            opacity:0.92;
        }

        .note{
            margin-top:18px;
            font-size:14px;
            opacity:0.9;
            line-height:1.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>صدقة جارية عن جدي عبدالرحمن بن جبران رحمه الله</h1>
        <div class="subtitle">
            أنشئ مسبحة إلكترونية لأي متوفى، ثم شارك الرابط ليتمكن الناس من التسبيح له والدعاء له.
        </div>

        <div class="card">
            <h2>إنشاء رابط مسبحة</h2>
            <form method="post" action="/create">
                <input type="text" name="name" placeholder="اكتب اسم المتوفى" required>
                <button type="submit">إنشاء المسبحة</button>
            </form>
        </div>

        <div class="note">
            كل رابط يتم إنشاؤه يكون خاصًا بالاسم الذي أدخلته، ويمكن لأي شخص فتحه والمشاركة في التسبيح.
        </div>
    </div>
</body>
</html>
"""


dhikr_page = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>المسبحة الإلكترونية</title>
    <style>
        *{
            box-sizing:border-box;
        }

        body{
            margin:0;
            font-family:Arial, sans-serif;
            background:linear-gradient(135deg,#020617,#111827,#1f2937);
            min-height:100vh;
            color:white;
            padding:24px;
        }

        .wrapper{
            max-width:750px;
            margin:0 auto;
            text-align:center;
        }

        .top-title{
            font-size:30px;
            margin-top:10px;
            line-height:1.7;
        }

        .small{
            opacity:0.9;
            margin-bottom:25px;
            line-height:1.8;
        }

        .stats{
            display:grid;
            grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));
            gap:14px;
            margin:25px 0;
        }

        .stat-box{
            background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:18px;
            padding:18px;
        }

        .stat-box h3{
            margin:0 0 10px 0;
            font-size:22px;
        }

        .stat-box p{
            margin:0;
            font-size:28px;
            font-weight:bold;
        }

        .main-card{
            background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:24px;
            padding:28px;
            box-shadow:0 20px 60px rgba(0,0,0,0.25);
        }

        .tasbih-button{
            width:100%;
            max-width:380px;
            height:90px;
            border:none;
            border-radius:24px;
            font-size:30px;
            font-weight:bold;
            color:white;
            cursor:pointer;
            margin:16px auto;
            display:block;
        }

        .subhan{background:#16a34a;}
        .hamd{background:#0284c7;}
        .akbar{background:#9333ea;}

        .tasbih-button:hover{
            opacity:0.92;
        }

        .link-box{
            margin-top:28px;
            background:rgba(255,255,255,0.06);
            border-radius:18px;
            padding:18px;
            text-align:right;
        }

        .link-box label{
            display:block;
            margin-bottom:10px;
            font-size:16px;
        }

        .link-input{
            width:100%;
            padding:14px;
            border-radius:12px;
            border:none;
            font-size:15px;
        }

        .back{
            display:inline-block;
            margin-top:20px;
            color:white;
            text-decoration:none;
            opacity:0.9;
        }

        .total{
            font-size:22px;
            margin-top:8px;
            color:#facc15;
            font-weight:bold;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="top-title">اللهم اغفر لـ {{ name }}</div>
        <div class="small">يمكن لأي شخص الدخول لهذا الرابط والمشاركة في التسبيح والدعاء.</div>

        <div class="total">إجمالي التسبيحات: {{ total }}</div>

        <div class="stats">
            <div class="stat-box">
                <h3>سبحان الله</h3>
                <p>{{ subhan }}</p>
            </div>
            <div class="stat-box">
                <h3>الحمدلله</h3>
                <p>{{ hamd }}</p>
            </div>
            <div class="stat-box">
                <h3>الله أكبر</h3>
                <p>{{ akbar }}</p>
            </div>
        </div>

        <div class="main-card">
            <form method="post">
                <button class="tasbih-button subhan" name="type" value="subhan">سبحان الله</button>
            </form>

            <form method="post">
                <button class="tasbih-button hamd" name="type" value="hamd">الحمدلله</button>
            </form>

            <form method="post">
                <button class="tasbih-button akbar" name="type" value="akbar">الله أكبر</button>
            </form>

            <div class="link-box">
                <label>انسخ الرابط وشاركه:</label>
                <input class="link-input" type="text" value="{{ link }}" readonly onclick="this.select();">
            </div>
        </div>

        <a class="back" href="/">الرجوع للصفحة الرئيسية</a>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(home_page)


@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "").strip()

    if not name:
        return redirect("/")

    person = Person(name=name)
    db.session.add(person)
    db.session.commit()

    return redirect(f"/dhikr/{person.id}")


@app.route("/dhikr/<int:id>", methods=["GET", "POST"])
def dhikr(id):
    person = Person.query.get_or_404(id)

    if request.method == "POST":
        dhikr_type = request.form.get("type")

        if dhikr_type == "subhan":
            person.subhan += 1
        elif dhikr_type == "hamd":
            person.hamd += 1
        elif dhikr_type == "akbar":
            person.akbar += 1

        db.session.commit()
        return redirect(f"/dhikr/{person.id}")

    link = request.host_url.rstrip("/") + url_for("dhikr", id=person.id)

    return render_template_string(
        dhikr_page,
        name=person.name,
        subhan=person.subhan,
        hamd=person.hamd,
        akbar=person.akbar,
        total=person.total,
        link=link
    )


import os

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)