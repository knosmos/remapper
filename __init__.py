import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import re
import pickle
import exiffer
#from flask_bootstrap import Bootstrap

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '\\images'
app.config['SECRET_KEY'] = 'mysupersupersecretkey'
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

MAP_ROUTE = []
mainpage_counter = 0

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

class User():
    def __init__(self, name,password):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        self.password = password
        try: self.id = unicode(name,'utf-8')
        except: self.id = name
    def get_id(self):
        return self.id

def handle_register(name,password,p):
    try:
        with open(p,'r') as f:
            userdata = pickle.load(f)
    except:
        userdata = []
    for i in userdata:
        if i.id == name:
            flash('Username already taken')
            return redirect(url_for('register'))
    userdata.append(User(name,password))
    with open(p,'w') as f:
        pickle.dump(userdata,f,2)

def parse_gpx(gpxFName):
    coords = []
    with open(gpxFName, 'rU') as fpIn:
        for line in fpIn:
            if 'trkpt lat' in line:
                # I know regular expressions!
                matches = re.search(r'.*lat=\"(.*\d+.\d+)\" lon=\"(.*\d+.\d+)\"', line)
                lat = float(matches.groups(0)[0])
                lon = float(matches.groups(0)[1])
                coords.append([lat, lon])
    return coords

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def retrieve_images(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk('static\\trips\\'+path):
        for file in f:
            if '.JPG' in file:
                files.append([path+'\\'+file])

@login_manager.user_loader
def load_user(id):
    print id
    return User(id,'123')

@app.route('/login',methods=['GET','POST'])
def login():
    global logged_on
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username,password)
        with open('users.pickle','r') as p:
            users = pickle.load(p)
        print users
        print username
        for i in users:
            if i.id == username:
                userdata = i
                break
        else:
            flash('Invalid Username')
            return redirect(url_for('mainpage'))
        if password == userdata.password:
            login_user(user)
            flash('Hi, '+username)
            return redirect(url_for('mainpage'))
        flash('Invalid Password')
        return redirect(url_for('login'))
    return render_template('login2.html')

@app.route('/register',methods=['GET','POST'])
def register():
    global logged_on
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        npass = request.form['password2']
        if password == npass:
            handle_register(username,password,'users.pickle')
            user = User(username,password)
            login_user(user)
            flash('Hi, '+username)
            return redirect(url_for('mainpage'))
        flash("Passwords Don't Match")
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/brian')
def brian():
    MAP_ROUTE = '[[35.39332,138.73388],[35.39254,138.73467],[35.39241,138.73526],[35.39166,138.7365],[35.3905,138.74017],[35.39035,138.74169],[35.38997,138.74217],[35.38914,138.74235],[35.3886,138.74265],[35.3882,138.74322],[35.38777,138.7434],[35.3861,138.74494],[35.38602,138.74554],[35.38562,138.74622],[35.38575,138.74642],[35.38538,138.74702],[35.38516,138.74774],[35.38481,138.74699],[35.38457,138.74718],[35.38456,138.74692],[35.38432,138.74725],[35.38295,138.74733],[35.38311,138.74688],[35.3827,138.74697],[35.38276,138.7465],[35.38266,138.7465],[35.38231,138.74687],[35.38193,138.74696],[35.38191,138.74675],[35.38165,138.74677],[35.38168,138.74635],[35.38131,138.74642],[35.3814,138.74597],[35.38094,138.74612],[35.38106,138.74554],[35.38068,138.74561],[35.38062,138.74523],[35.38016,138.74533],[35.38019,138.7451],[35.37998,138.74518],[35.37995,138.74494],[35.37978,138.74501],[35.37982,138.7447],[35.37952,138.74466],[35.3796,138.74433],[35.37906,138.74434],[35.37877,138.74471],[35.37859,138.74449],[35.37879,138.74424],[35.37873,138.74405],[35.37864,138.74396],[35.37853,138.74414],[35.37838,138.74408],[35.37829,138.74357],[35.37788,138.7438],[35.37761,138.74368],[35.37776,138.74354],[35.37762,138.74341],[35.37733,138.7435],[35.37739,138.74289],[35.37699,138.74303],[35.37695,138.74283],[35.37663,138.74297],[35.37625,138.74275],[35.37575,138.74312],[35.37558,138.7429],[35.37523,138.743],[35.37496,138.74242],[35.37454,138.74234],[35.37421,138.74142],[35.374,138.74157],[35.37383,138.74151],[35.37382,138.74121],[35.37354,138.74093],[35.37325,138.74114],[35.37289,138.74097],[35.37288,138.74016],[35.37248,138.74042],[35.37248,138.74007],[35.37231,138.74009],[35.37217,138.73977],[35.372,138.73971],[35.37156,138.74001],[35.37169,138.73954],[35.37157,138.73898],[35.37147,138.73895],[35.37136,138.73914],[35.3712,138.73866],[35.37098,138.73936],[35.37092,138.73928],[35.37068,138.73942],[35.37057,138.73884],[35.37042,138.73912],[35.37037,138.73889],[35.37008,138.7392],[35.36992,138.7386],[35.36976,138.73883],[35.36965,138.73856],[35.36911,138.73917],[35.36927,138.73885],[35.36919,138.73877],[35.36896,138.73894],[35.36879,138.73876],[35.3689,138.73848],[35.36867,138.7384],[35.36868,138.73818],[35.36812,138.73797],[35.36844,138.73774],[35.36818,138.73765],[35.3683,138.7374],[35.36769,138.73735],[35.36801,138.73714],[35.36786,138.73704],[35.36798,138.73689],[35.36774,138.73678],[35.36786,138.73661],[35.36753,138.73642],[35.36747,138.73604],[35.36722,138.73594],[35.36731,138.73577],[35.36713,138.73577],[35.36723,138.7356],[35.36699,138.73534],[35.36704,138.73513],[35.36684,138.73511],[35.36685,138.7349],[35.36662,138.73476],[35.3667,138.73469],[35.36644,138.73466],[35.36656,138.73442],[35.36631,138.73428],[35.36635,138.73383],[35.36575,138.7334],[35.36558,138.73342],[35.36582,138.73281],[35.36565,138.73296],[35.36559,138.73277],[35.36568,138.73273],[35.36565,138.73298],[35.36557,138.7329],[35.36534,138.73312],[35.36575,138.73292],[35.36568,138.73268],[35.36564,138.73299],[35.36556,138.73289],[35.365,138.73332],[35.36488,138.73325],[35.36435,138.7339],[35.36358,138.73418],[35.36271,138.73435],[35.3622,138.73404],[35.36095,138.73386],[35.36054,138.73357],[35.36039,138.73302],[35.35987,138.73229],[35.35986,138.73207],[35.36005,138.73185],[35.35958,138.73149],[35.35962,138.73079],[35.35923,138.73082],[35.35967,138.73076],[35.35966,138.73101],[35.35987,138.72937],[35.35973,138.72907],[35.35978,138.72835],[35.36054,138.7273],[35.36064,138.72732],[35.36047,138.72755],[35.3613,138.7272],[35.36198,138.72714],[35.36271,138.72751],[35.36314,138.72703],[35.36381,138.72697],[35.36466,138.72724],[35.36495,138.72813],[35.36475,138.72854],[35.36478,138.72899],[35.36546,138.72941],[35.36634,138.73135],[35.36602,138.7327],[35.36531,138.7331],[35.36627,138.73538],[35.3649,138.73344],[35.36458,138.73437],[35.36372,138.73535],[35.36519,138.73571],[35.36557,138.73558],[35.36527,138.73621],[35.36464,138.7368],[35.36469,138.73688],[35.36555,138.737],[35.36642,138.73681],[35.3657,138.73821],[35.36774,138.73819],[35.36886,138.73939],[35.36853,138.73968],[35.36921,138.74022],[35.36885,138.74064],[35.36892,138.74085],[35.36941,138.74126],[35.37056,138.74107],[35.37069,138.74088],[35.37068,138.7411],[35.3703,138.74169],[35.37103,138.74157],[35.37049,138.7424],[35.37121,138.74231],[35.37058,138.74319],[35.37178,138.74282],[35.37125,138.74351],[35.37227,138.74334],[35.37166,138.74445],[35.37293,138.74457],[35.37252,138.74526],[35.37388,138.74536],[35.37364,138.74582],[35.37414,138.74592],[35.37387,138.74626],[35.37435,138.74632],[35.37411,138.7468],[35.37463,138.74686],[35.37441,138.74733],[35.37485,138.74734],[35.37463,138.74784],[35.37506,138.74785],[35.37479,138.74833],[35.37528,138.7483],[35.37499,138.74881],[35.37552,138.74887],[35.37529,138.74931],[35.3758,138.74932],[35.37553,138.7498],[35.37602,138.74986],[35.37579,138.75029],[35.37622,138.7503],[35.37593,138.75087],[35.37652,138.75086],[35.37623,138.75138],[35.37672,138.75144],[35.3764,138.75207],[35.37759,138.75202],[35.37827,138.75119],[35.37909,138.75052],[35.38043,138.75009],[35.38122,138.74937],[35.38123,138.74961],[35.38188,138.74908],[35.38219,138.74906],[35.38317,138.748],[35.38445,138.74707],[35.38447,138.74717],[35.38455,138.74685],[35.3846,138.74718],[35.38482,138.74695],[35.38507,138.74759],[35.38524,138.74761],[35.38594,138.74583],[35.38611,138.7449],[35.38775,138.74335],[35.38821,138.74319],[35.38871,138.74262],[35.38926,138.74245],[35.38951,138.74222],[35.38983,138.74227],[35.39009,138.74205],[35.39036,138.7415],[35.39049,138.7402],[35.39087,138.73888],[35.39187,138.73588],[35.39241,138.73505],[35.39252,138.73458],[35.39427,138.73318]];'
    coords=[[35.39028, 138.74139], [35.37417, 138.74167], [35.37167, 138.73944], [35.36889, 138.73889], [35.36806, 138.73722], [35.36722, 138.73611], [35.36556, 138.73278], [35.36, 138.73167], [35.35944, 138.73111], [35.36056, 138.72722], [35.36472, 138.73361], [35.36917, 138.74111], [35.37111, 138.74333], [35.37778, 138.75167], [35.39361, 138.73361], [35.39417, 138.73306]]
    images=[['Mt_Fuji\\IMG_2807.JPG','Mt_Fuji\\IMG_2807.JPG','Mt_Fuji\\IMG_2807.JPG'], ['Mt_Fuji\\IMG_2872.JPG'], ['Mt_Fuji\\IMG_2920.JPG'], ['Mt_Fuji\\IMG_2943.JPG'], ['Mt_Fuji\\IMG_2962.JPG'], ['Mt_Fuji\\IMG_3005.JPG'], ['Mt_Fuji\\IMG_3031.JPG'], ['Mt_Fuji\\IMG_3055.JPG'], ['Mt_Fuji\\IMG_3061.JPG'], ['Mt_Fuji\\IMG_3072.JPG'], ['Mt_Fuji\\IMG_3129.JPG'], ['Mt_Fuji\\IMG_3148.JPG'], ['Mt_Fuji\\IMG_3153.JPG'], ['Mt_Fuji\\IMG_3157.JPG'], ['Mt_Fuji\\IMG_3164.JPG'], ['Mt_Fuji\\IMG_3172.JPG']]
    points=['Climbing Route Sign', 'Long Way Up', 'Cloud Cover', 'Rest Stop', 'Sunrise', 'Sunrise', 'Mountaintop Structure', 'Crater', 'Gate', 'Markers', 'At the Peak', 'Sign', 'Plants', 'Through this way', 'Back at the Entrance' , 'Final Stop']
    comments=['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    return render_template('interactivetrip.html',points=points,comments=comments,name="Sunrise at Mt. Fuji",images=images,imgcoords=coords,route=MAP_ROUTE)

@app.route('/view')
def view():
    user = request.args.get('author')
    name=request.args.get('name')
    dname=name.replace('_',' ')
    try:
        maptype='mapbox.'+request.args.get('type')
    except:
        maptype='mapbox.satellite'
    #images=[['jauntimages\\IMG_5690.JPG', 'jauntimages\\IMG_5691.JPG', 'jauntimages\\IMG_5694.JPG'], ['jauntimages\\IMG_5741.JPG','jauntimages\\IMG_5742.JPG'], ['jauntimages\\IMG_5745.JPG', 'jauntimages\\IMG_5746.JPG', 'jauntimages\\IMG_5747.JPG'], ['jauntimages\\IMG_5765.JPG'], ['jauntimages\\IMG_5797.JPG', 'jauntimages\\IMG_5799.JPG', 'jauntimages\\IMG_5719.JPG']]
    #coords=[[40.37194, -74.63389], [40.37222, -74.63417], [40.37222, -74.63417], [40.37194, -74.63528], [40.375, -74.63222]]
    #points=['Red Tree','Entrance to Trail','Road Down','More Trail','Lake','Bend in the Path','Someplace']
    #comments=['Pretty Fall Foilage','Trees, trees, trees','It is actually quite short',' ',' ','Hard to see the road because of all the leaves','Yeah. Somewhere.']
    with open('static/users/'+user+'/'+name+'/data.pickle','rb') as datafile:
        data=pickle.load(datafile)
        coords = data['coords']
        images = data['images']
        MAP_ROUTE = data['route']#.replace('var positions = ','')
        comments = []
        points = []
        for _ in range(len(images)):
            comments.append('hello')
            points.append('hi')
    return render_template('interactivetrip.html',points=points,comments=comments,name=dname,images=images,imgcoords=coords,route=MAP_ROUTE,maptype=maptype)

@app.route('/embed')
def embed():
    user = request.args.get('author')
    name=request.args.get('name')
    dname=name.replace('_',' ')
    try:
        maptype='mapbox.'+request.args.get('type')
    except:
        maptype='mapbox.satellite'
    with open('static/users/'+user+'/'+name+'/data.pickle','rb') as datafile:
        data=pickle.load(datafile)
        coords = data['coords']
        images = data['images']
        MAP_ROUTE = data['route']
        comments = []
        points = []
        for _ in range(len(images)):
            comments.append('hello')
            points.append('hi')
    return render_template('embedtripv2.html',points=points,comments=comments,name=dname,images=images,imgcoords=coords,route=MAP_ROUTE,maptype=maptype)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def mainpage():
    global logged_on, mainpage_counter
    #return render_template('allmaps.html')
    trips = []
    print(current_user.id)
    user = current_user.id.encode('utf8')
    for r, d, f in os.walk('static\\users\\'+user):
        for di in d:
            trips.append(di)
        break
    print trips
    thumbs = []
    for i in trips:
        for r, d, f in os.walk('static\\users\\'+user+'\\'+i+'\\images'):
            thumbs.append('static/users/'+user+'/'+i+'/images/'+f[0])
    dtrips = []
    for i in trips: 
        dtrip = ''
        si = i.replace('_',' ').split(' ')
        for j in si:
            dtrip+=j.capitalize()
            dtrip+=' '
        dtrip=dtrip[:-1]
        dtrips.append(dtrip)
    print thumbs
    print dtrips
    return render_template('newmain.html',tripnames=dtrips,tripurls=trips,thumbnailimgs=thumbs)

@login_required
@app.route('/new', methods=['GET', 'POST'])
def upload_file():
    global MAP_ROUTE, logged_on
    if request.method == 'POST':
        user = current_user.id.encode('utf-8')
        print(request.files)
        name = request.form['name'].replace(' ','_')
        print(name)
        images = request.files.getlist('images')
        gpxfile = request.files['gpxfile']
        print(images)
        imagefilenames = []
        os.makedirs('static/users/'+user+'/'+name+'/images')
        for f in images:
            filename = secure_filename(f.filename)
            f.save('static/users/'+user+'/'+name+'/images/'+filename)
        target_gpxfile = 'static/users/'+user+'/'+name+'/'+secure_filename(gpxfile.filename)
        gpxfile.save(target_gpxfile)
        print(user+'/'+name)
        images,coords=exiffer.return_gps(str(user+'\\'+name))
        print(images)
        print(coords)
        if '.gpx' in target_gpxfile: MAP_ROUTE = parse_gpx(target_gpxfile)
        else:
            with open(target_gpxfile) as f:
                MAP_ROUTE = f.read()
        data = {'images':images,'coords':coords,'route':MAP_ROUTE}
        with open('static/users/'+user+'/'+name+'/data.pickle','wb') as datafile:
            pickle.dump(data,datafile,2)
        return render_template('edittripv3.html',name=name.replace('_',' '),images=images,imgcoords=coords,route=MAP_ROUTE)
    return render_template('newtrip.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__=='__main__':
    app.run(host='0.0.0.0')
