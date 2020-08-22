from model.base import create_app
from app.timeline import timeapi as T
from app.tags import tagapi as Ta
from app.about import aboutapi as ab
from app.homepage import blogapi as home
from app.search import ser as ser
from app.admin import adminapi as ad

app = create_app()

app.register_blueprint(ab)
app.register_blueprint(T)
app.register_blueprint(Ta)
app.register_blueprint(home)
app.register_blueprint(ser)
app.register_blueprint(ad)

if __name__=="__main__":
    app.run(debug=True)