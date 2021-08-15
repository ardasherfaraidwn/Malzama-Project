from flask import Blueprint,render_template,request,flash,redirect, url_for
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import current_date
from .models import Students,Malzama,info,Malzama_tp
from . import db


views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
def home():
    students_name = db.session.query(Students)
    malzama_name = db.session.query(Malzama)
    if request.method == 'POST':
        selc = request.form.getlist('st')
        malzama_subject = int(request.form.get("st2_malzama"))
        for student_ids in selc:
            l = []
            all_students = db.session.query(info.malzama_id).filter_by(student_id=student_ids).all()
            for student in all_students:
                for id in student:
                    l.append(id)
            if malzama_subject in l:
                current_st = db.session.query(Students).get(student_ids)
                flash(current_st.st_name+" has got malzama already",category="error")
                l.clear()

            else:
                new_data = info(student_id=student_ids,malzama_id=malzama_subject)
                db.session.add(new_data)
                db.session.commit()
                current_st = db.session.query(Students).get(student_ids)
                flash(current_st.st_name,category="success")
                l.clear()

    return render_template('index.html',students_name=students_name,malzama=malzama_name)




@views.route('/malzama',methods=['GET','POST'])
def malzama():
    all_types = Malzama_tp.query.all()
    all_malzama = db.session.query(Malzama,Malzama_tp).join(Malzama_tp).all()
    if request.method == 'POST':
        malzama_input = request.form.get("add_malzama")
        malzama_subject = request.form.get("subject")
        new_malzama = Malzama(mz_name=malzama_input,mz_category=malzama_subject)
        db.session.add(new_malzama)
        db.session.commit()
        flash(f"{malzama_input} added to database",category="success")
    return render_template('malzama.html',typess=all_types,malzamas = all_malzama)




@views.route('/cetegores',methods=['GET','POST'])
def cetegory():
    all_types = Malzama_tp.query.all()
    if request.method == 'POST':
        type_input = request.form.get("add_type")
        new_type = Malzama_tp(typee=type_input)
        db.session.add(new_type)
        db.session.commit()
        flash(f"{type_input} added to database",category="success")
    return render_template('category.html',data=all_types)


# this route is for creating profile for subjects
@views.route('/cetegores/update/<int:id>',methods=['GET','POST'])
def type_profile(id):
    current_date = Malzama_tp.query.get(id);
    if request.method == 'POST':
        type_input = request.form.get("edit_type")
        new_type = Malzama_tp.query.get(id)
        new_type.typee = type_input
        db.session.commit()
        flash(f"successfully updated to {new_type.typee}",category="success")
    return render_template('edit_type.html',data=current_date)

# this route for deleting profiles
@views.route('/cetegores/delete/<int:id>')
def type_delete(id):
    current_date = Malzama_tp.query.filter_by(id=id);
    current_date.delete();
    db.session.commit()
    # flash(f"successfully updated to {new_type.typee}",category="success")
    return redirect("http://127.0.0.1:5000/cetegores",code=302)

# this route for deleting malzama
@views.route('/malzama/delete/<int:id>')
def malzama_delete(id):
    current_date = Malzama.query.filter_by(id=id);
    current_date.delete();
    db.session.commit()
    # flash(f"successfully updated to {new_type.typee}",category="success")
    return redirect("http://127.0.0.1:5000/malzama",code=302)


#this toute for info database show student information
@views.route('/info',methods=['GET','POST'])
def info_page():
    studentes = Students.query.all()
    if request.method == "POST":
        selected_st = request.form.get("st_search")
        data = db.session.query(info,Malzama,Students).join(Malzama,Students).filter_by(id=selected_st)
        return render_template('info.html',data=data,studentes=studentes)
    # flash(f"successfully updated to {new_type.typee}",category="success")
    return render_template('info.html',studentes=studentes)