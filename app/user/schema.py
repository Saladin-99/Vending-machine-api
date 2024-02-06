from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import ma
from app.user.model import User
from marshmallow import post_dump, validates, ValidationError, validate

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

    # Add validation settings for fields
    id = ma.auto_field(dump_only=True)
    username = ma.String(required=True, validate=validate.Length(min=1, max=30))
    password = ma.String(required=True, validate=validate.Length(min=6, max=30))
    deposit = ma.Float(default=0.0)
    role = ma.String(required=True, validate=validate.OneOf(['buyer', 'seller']))

    # Custom validation method for a specific field
    @validates('deposit')
    def validate_deposit(self, value):
        if value < 0:
            raise ValidationError('Deposit must be non-negative.')

#    @post_dump
#    def process_relationships(self, data, **kwargs):
#        # Load the 'products' relationship before serialization
#        if 'products' in data:
#            data['products'] = product_schema.dump(data['products'], many=True)
#        return data
