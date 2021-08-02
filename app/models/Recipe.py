from app import db


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("recipe", lazy=True))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime)

    def __repr__(self):
        return self.name
