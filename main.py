#Import begin
#Flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

#SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Database
from database_setup import Restaurant, Base, MenuItem
#Import end

#Create DB session
engine = create_engine('sqlite:///restaurantmenu.db', echo=True, connect_args={"check_same_thread": False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Create Flask app
app = Flask(__name__)

@app.route('/restaurants/<int:restaurantId>/JSON')
def displayMenuItemsJson(restaurantId):
    restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
    menus = session.query(MenuItem).filter_by(restaurant_id = restaurantId)
    return jsonify(menus=[i.serialize for i in menus])

@app.route('/restaurants/<int:restaurantId>/menu/<int:menuId>/JSON')
def displayMenuItemJson(restaurantId, menuId):
    menu = session.query(MenuItem).filter_by(id = menuId).one()
    return jsonify(menu=menu.serialize)

@app.route('/restaurants/<int:restaurantId>/')
def displayMenuItems(restaurantId):
    restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
    menus = session.query(MenuItem).filter_by(restaurant_id = restaurantId)
    return render_template('menus.html', restaurant = restaurant, items = menus)

@app.route('/restaurants/<int:restaurantId>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurantId):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurantId)
        session.add(newItem)
        session.commit()
        flash('New item added!')
        return redirect(url_for('displayMenuItems', restaurantId=restaurantId))
    else:
        return render_template('newmenuitem.html', restaurantId=restaurantId)

@app.route('/restaurants/<int:restaurantId>/<int:menuId>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurantId, menuId):
    editedItem = session.query(MenuItem).filter_by(id=menuId).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('New item edited!')
        return redirect(url_for('displayMenuItems', restaurantId=restaurantId))
    else:
        return render_template('editmenuitem.html', restaurantId=restaurantId, menuId=menuId, item=editedItem)
    return output
   
@app.route('/restaurants/<int:restaurantId>/<int:menuId>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurantId, menuId):
    deletedItem = session.query(MenuItem).filter_by(id=menuId).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('New item deleted!')
        return redirect(url_for('displayMenuItems', restaurantId=restaurantId))
    else:
        return render_template('deletemenuitem.html', restaurantId=restaurantId, item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'password'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
