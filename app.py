# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 10:50:33 2021

@author: Sayam
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

contact_put_args = reqparse.RequestParser()
contact_put_args.add_argument("username", type=str, help="UserName of the Contact is required", required=True)
contact_put_args.add_argument("firstname", type=str, help="FirstName of the contact", required=True)
contact_put_args.add_argument("lastname", type=str, help="LastName on the contact", required=True)

email_put_args = reqparse.RequestParser()
email_put_args.add_argument("subject", type=str, help="Subject of the email", required=True)
email_put_args.add_argument("message", type=str, help="Message on the email", required=True)
email_put_args.add_argument("contact_id", type=int, help="ID of the contact", required=True)



contact_update_args = reqparse.RequestParser()
contact_update_args.add_argument("username", type=str, help="UserName of the Contact is required")
contact_update_args.add_argument("firstname", type=str, help="FirstName of the contact")
contact_update_args.add_argument("lastname", type=str, help="LastName on the contact")





class ContactModel(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    emails = db.relationship('EmailModel', backref='contacts')
    
    def __repr__(self):
        return f"contact(id= {id}, username = {username}, firstname = {firstname}, lastname = {lastname})"





class EmailModel(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    
    def __repr__(self):
        print("Here")
        return f"email(id= {id}, subject = {subject}, message = {message}, contact_id = {contact_id})"

    
    
#db.create_all()


resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    }


email_resource_fields = {
    'id': fields.Integer,
    'subject': fields.String,
    'message': fields.String,
    'contactId': fields.Integer
    }




class Contacts(Resource):
    
    @marshal_with(resource_fields)
    def get(self):

        result = ContactModel.query.all()
        if not result:
            abort(404, message = "Contact not found")
        return result
    
    
    
    
    
class Contact(Resource):
    
    @marshal_with(resource_fields)
    def get(self, User):
        #print("username: ",User)
        result = ContactModel.query.filter_by(username = User).first()
        #print(result)
        if not result:
            abort(404, message = "Contact not found")
        return result
      
    
    
    @marshal_with(resource_fields)
    def put(self, contactId):
        args = contact_put_args.parse_args()
        print("Arguments", args)
        result = ContactModel.query.filter_by(id = contactId).first()
        if result:
            abort(409, message = "Contact already exists")

        contact = ContactModel(id = contactId, username = args['username'], firstname = args["firstname"], lastname = args["lastname"])
        db.session.add(contact)
        db.session.commit()
        return contact, 201
    
    @marshal_with(resource_fields)
    def patch(self,contactId):
        args = contact_update_args.parse_args()
        
        result = ContactModel.query.filter_by(id = contactId).first()
        if not result:
            abort(404, message = "Contact doesn't exist")
        
        if args['username']:
            result.username = args['username']
        if args['firstname']:
            result.firstname = args['firstname']
        if args['lastname']:
            result.lastname = args['lastname']
            
        db.session.commit()
        return result
    
    def delete(self,contactId):
        result = ContactModel.query.filter_by(id = contactId).delete()
        db.session.commit()
        if not result:
            abort(404, message = "Contact doesn't exist")
        return "Deleted Succesfully", 204
    
    
    
    
    
    
class Email(Resource):
    @marshal_with(email_resource_fields)
    def put(self, Id):
        args = email_put_args.parse_args()
        print("Arguments", args)
        result = EmailModel.query.filter_by(id = Id).first()
        
        if result:
            abort(409, message = "Email already exists")
        email = EmailModel(id = Id, subject = args['subject'], message = args["message"], contact_id = args["contact_id"])

        db.session.add(email)
        db.session.commit()
        return email, 201
    
    @marshal_with(email_resource_fields)
    def get(self, Id):
        result = EmailModel.query.filter_by(contact_id = Id).first()

        if not result:
            abort(404, message = "Email not found")
        return result    



api.add_resource(Contact,"/contact/<string:User>", "/contact/<int:contactId>")
api.add_resource(Contacts, "/contacts")
api.add_resource(Email, "/email/<int:Id>")

if __name__ == '__main__':
    app.run()
