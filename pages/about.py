from dash import html
from pages.home import get_sidebar

def get_about_page(active_item="about"):
    return html.Div(
        children=[
            get_sidebar(active_item=active_item),
            html.Div(
                children=[
                    html.H3("Our Team", className="text-center mt-5"),
                    html.Ul(
                        children=[
                            html.Li("Trịnh Minh Anh - 21280005"),
                            html.Li("Lê Hồ Hoàng Anh - 21280085"),
                            html.Li("Nguyễn Phúc Loan - 21280098"),
                        ],
                        className="list-unstyled text-center",
                    ),
                    html.P(
                        "We are a group of passionate professionals working together to make a difference. ;))) ",
                        className="lead text-center mt-4",
                    ),
                    html.Img(
                        src="/assets/success_kid.jpg", 
                        className="img-fluid mt-4",  
                        style={"maxWidth": "80%", "margin": "0 auto", "display": "block", 'height': '300px'}, 
                    ),
                ],
                className="about-content", 
            ),
        ],
    )
