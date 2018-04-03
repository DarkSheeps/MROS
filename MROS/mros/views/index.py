from flask import Flask, render_template, request, redirect, session, Blueprint
from mros.tools.db_helper import SQLHelper
from wtforms import Form
from wtforms.fields import simple
from wtforms.fields import html5
from wtforms.fields import core
from wtforms import widgets
from wtforms import validators
import functools
import json
import datetime

index = Blueprint('index', __name__, url_prefix='/index')


@index.before_request
def token():
    user = session.get('user_id')
    if not user:
        return redirect('/account')


@index.route('/reserve', methods=['GET', 'POST'], endpoint='reserve')
def reserveRoom():
    if request.method == "GET":
        if request.args.get('date'):
            date = request.args.get('date')
        else:
            date = datetime.date.today()

        rooms_sql = 'SELECT * from meeting_room'
        reserve_room_sql = 'SELECT * from reserve WHERE reserve_date like %s'
        times_sql = 'SELECT * from TIME '
        rooms = SQLHelper.fetch_all(rooms_sql, [])
        reserve_rooms = SQLHelper.fetch_all(reserve_room_sql, [date,])
        times = SQLHelper.fetch_all(times_sql, [])
        user_id = session.get('user_id')

        """
            msg={
                room_id:{
                    name:room_name,
                    times:[{},{}]
                }
            }

        """

        msg = {}

        for room in rooms:
            msg[room['mid']] = {
                'name': room['rname'],
                'time_list': times
            }

        r_time_dict = {}
        """
            {
                room_id:[time_id,time_id,]
            }
        """
        for r_room in reserve_rooms:

            if not r_time_dict.get(r_room['room_id']):
                r_time_dict[r_room['room_id']] = [r_room['time_id'],]
            else:
                r_time_dict[r_room['room_id']].append(r_room['time_id'])

        # print(r_time_dict)
        return render_template('index.html', times=times, msg=msg, r_time_dict=r_time_dict, current_user_id=user_id)

    else:
        ret = {'code': 800, 'msg': None}
        try:
            choiceDate = request.form.get('choiceDate')
            choice_time = int(request.form.get('choiceTime'))
            choice_room = int(request.form.get('choiceRoom'))
            user_id = session.get('user_id')
            s = choiceDate.split('-')
            choice_date = datetime.date(year=int(s[0]), month=int(s[1]), day=int(s[2]))

            mysql = 'insert into reserve(reserve_date,user_id,room_id,time_id) values(%s,%s,%s,%s);'
            SQLHelper.execute_one(mysql, [choice_date, user_id, choice_room, choice_time])

        except Exception as e:
            print('post...    ', e)
            ret['code'] = 804
            ret['msg'] = '预约失败'

        data = json.dumps(ret)
        return data


@index.route('/delete', methods=['GET', 'POST'], endpoint='delete')
def deleteRoom():
    if request.method == "GET":
        pass
    else:
        ret = {'code': 800, 'msg': None}
        try:
            choiceDate = request.form.get('choiceDate')
            choice_time = int(request.form.get('choiceTime'))
            choice_room = int(request.form.get('choiceRoom'))
            user_id = session.get('user_id')

            s = choiceDate.split('-')
            choice_date = datetime.date(year=int(s[0]), month=int(s[1]), day=int(s[2]))

            mysql = 'delete from reserve where reserve_date=%s AND room_id=%s AND time_id=%s'
            SQLHelper.delete_msg(mysql, [choice_date, choice_room, choice_time,])

        except Exception as e:
            print('post...    ', e)
            ret['code'] = 804
            ret['msg'] = '预约失败'

        data = json.dumps(ret)
        return data
