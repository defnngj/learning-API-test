from flask import Flask
from flask_graphql import GraphQLView

from schema import Schema

app = Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=Schema,
    graphiql=True,
))

# Optional, for adding batch query support (used in Apollo-Client)
app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
    'graphql',
    schema=Schema,
    batch=True
))

if __name__ == '__main__':
    app.run()
