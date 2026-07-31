import pandas as pd

from ydata_profiling import ProfileReport

df = pd.read_csv("video_game_sales.csv")

profile = ProfileReport(

    df,

    title="Video Game Sales Profile",

    explorative=True

)

profile.to_file("video_game_sales_profile.html")
