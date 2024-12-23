from app import app
import psycopg
from flask import render_template

@app.route('/schedule/<group>/<teacher>/<corp>/<aud>', methods=['GET', 'POST'])
def scheduleShow(group, teacher, corp, aud):
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()

        if group == 'не выбрано' and teacher == 'не выбрано' and corp != 'не выбрано' and aud != 'не выбрано':
            title = f"Расписание для корпус {corp}, ауд. {aud}"
            rasp = cur.execute('SELECT group_number, week_type, week_day, class_number, class_course_name, full_name, building_address, room_number '
                               'FROM group_class JOIN class USING (week_day, class_number, week_type, building_address, room_number) '
                               'JOIN teacher ON class.teacher_emp_record_num = teacher.emp_record_num '
                               'JOIN day_of_week ON week_day = day_of_week.day '
                               'WHERE building_address = %s AND room_number = %s '
                               'ORDER BY week_type, day_number', (corp, aud,)).fetchall()

        elif group == 'не выбрано' and teacher != 'не выбрано' and corp == 'не выбрано' and aud == 'не выбрано':
            title = f"Расписание для преподавателя {teacher}"
            rasp = cur.execute('SELECT group_number, week_type, week_day, class_number, class_course_name, full_name, building_address, room_number '
                               'FROM group_class JOIN class USING (week_day, class_number, week_type, building_address, room_number) '
                               'JOIN teacher ON class.teacher_emp_record_num = teacher.emp_record_num '
                               'JOIN day_of_week ON week_day = day_of_week.day '
                               'WHERE full_name = %s '
                               'ORDER BY week_type, day_number', (teacher,)).fetchall()

        elif group == 'не выбрано' and teacher != 'не выбрано' and corp != 'не выбрано' and aud != 'не выбрано':
            title = f"Расписание для преподавателя {teacher}, корпус {corp}, ауд. {aud}"
            rasp = cur.execute('SELECT group_number, week_type, week_day, class_number, class_course_name, full_name, building_address, room_number '
                               'FROM group_class JOIN class USING (week_day, class_number, week_type, building_address, room_number) '
                               'JOIN teacher ON class.teacher_emp_record_num = teacher.emp_record_num '
                               'JOIN day_of_week ON week_day = day_of_week.day '
                               'WHERE full_name = %s AND building_address = %s AND room_number = %s '
                               'ORDER BY week_type, day_number', (teacher, corp, aud,)).fetchall()

        elif group != 'не выбрано' and teacher == 'не выбрано' and corp == 'не выбрано' and aud == 'не выбрано':
            title = f"Расписание для группы {group}"
            rasp = cur.execute('SELECT group_number, week_type, week_day, class_number, class_course_name, full_name, building_address, room_number '
                               'FROM group_class JOIN class USING (week_day, class_number, week_type, building_address, room_number) '
                               'JOIN teacher ON class.teacher_emp_record_num = teacher.emp_record_num '
                               'JOIN day_of_week ON week_day = day_of_week.day '
                               'WHERE group_number = %s '
                               'ORDER BY week_type, day_number', (group,)).fetchall()

        elif group != 'не выбрано' and teacher == 'не выбрано' and corp != 'не выбрано' and aud != 'не выбрано':
            title = f"Расписание для группы {group}, корпус {corp}, ауд. {aud}"
            rasp = cur.execute('SELECT group_number, week_type, week_day, class_number, class_course_name, full_name, building_address, room_number '
                               'FROM group_class JOIN class USING (week_day, class_number, week_type, building_address, room_number) '
                               'JOIN teacher ON class.teacher_emp_record_num = teacher.emp_record_num '
                               'JOIN day_of_week ON week_day = day_of_week.day '
                               'WHERE group_number = %s AND building_address = %s AND room_number = %s '
                               'ORDER BY week_type, day_number', (group, corp, aud,)).fetchall()

        elif group != 'не выбрано' and teacher != 'не выбрано' and corp == 'не выбрано' and aud == 'не выбрано':
            title = f"Расписание для группы {group}, преподавателя {teacher}"
            rasp = cur.execute('SELECT group_number, week_type, week_day, class_number, class_course_name, full_name, building_address, room_number '
                               'FROM group_class JOIN class USING (week_day, class_number, week_type, building_address, room_number) '
                               'JOIN teacher ON class.teacher_emp_record_num = teacher.emp_record_num '
                               'JOIN day_of_week ON week_day = day_of_week.day '
                               'WHERE group_number = %s AND full_name = %s '
                               'ORDER BY week_type, day_number', (group, teacher,)).fetchall()

        elif group != 'не выбрано' and teacher != 'не выбрано' and corp != 'не выбрано' and aud != 'не выбрано':
            title = f"Расписание для группы {group}, преподавателя {teacher}, корпус {corp}, ауд. {aud}"
            rasp = cur.execute('SELECT group_number, week_type, week_day, class_number, class_course_name, full_name, building_address, room_number '
                               'FROM group_class JOIN class USING (week_day, class_number, week_type, building_address, room_number) '
                               'JOIN teacher ON class.teacher_emp_record_num = teacher.emp_record_num '
                               'JOIN day_of_week ON week_day = day_of_week.day '
                               'WHERE group_number = %s AND full_name = %s AND building_address = %s AND room_number = %s '
                               'ORDER BY week_type, day_number', (group, teacher, corp, aud,)).fetchall()

    return render_template('scheduleShow.html', title=title, rasp=rasp)
