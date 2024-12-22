from flask import Flask
from flask_bootstrap import Bootstrap5
from app.config import Config
from flask_login import LoginManager

app = Flask(__name__)

bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object(Config)

from app import routes
from app import groups
from app import teachers
from app import directions
from app import edPlanShow
from app import courses

from app import scheduleForm
from app import scheduleShow

from app import editGroup
from app import updateGroupForm
from app import insertGroupForm
from app import deleteGroupForm

from app import editStream
from app import insertStreamForm
from app import deleteStreamForm

from app import editTeacher
from app import updateTeacherForm
from app import insertTeacherForm
from app import deleteTeacherForm

from app import editSchedule
from app import insertScheduleForm
from app import deleteScheduleForm
from app import updateSchedule
from app import updateScheduleForm

from app import editEdPlan
from app import insertPlanForm
from app import deletePlanForm
from app import deleteEdplan
from app import updateEdplan
from app import updatePlanForm

from app import editCourse
from app import updateCourseForm
from app import insertCourseForm
from app import deleteCourseForm

from app import adminRegForm
from app import adminLoginForm
from app import adminLogout