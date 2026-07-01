import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Amazon Music Song Clustering",
    page_icon="🎵",
    layout="wide"
)

df = pd.read_csv("clustered_songs.csv")

page = st.sidebar.radio(
    "Amazon Music Song Clustering",
    ["📊 Analysis","🎼 Cluster Summary","⭐ Top Songs","🔍 Song Search"]
)   

if page == "📊 Analysis":

    st.title("🎵 Amazon Music Song Clustering")

    st.write("""
    
    Millions of songs are available on music platforms.
    This project groups songs into clusters using their audio features
    like danceability, energy, tempo and acousticness.

    The objective is to identify songs with similar characteristics
    without using genre labels.
    """)


    st.header("📊 Clustering Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Optimal Clusters", "3")

    with col2:
        st.metric("Silhouette Score", "0.2378")

    with col3:
        st.metric("Davies-Bouldin Index", "1.57")


    st.info("""
    **Interpretation**

    • Elbow Method suggested **3 clusters**.

    • Silhouette Score (0.2378) indicates moderate cluster separation, which is acceptable for a large real-world music dataset.

    • Davies-Bouldin Index (1.57) indicates reasonable separation between clusters.
    """)    

    st.markdown("---")

    st.subheader("Elbow Method")

    st.image("elbow_method.png")

    st.markdown("---")

    st.subheader("PCA Visualization")

    st.image("pca.png")

    st.markdown("---")

    st.subheader("Cluster Heatmap")

    st.image("heatmap.png")   



elif page == "🎼 Cluster Summary":

    st.title("🎼 Cluster Summary")

    st.write(
        "Average values of the audio features for each cluster."
    )

    cluster_summary = df.groupby("Cluster")[
        [
            "danceability",
            "energy",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms"
        ]
    ].mean()

    st.dataframe(cluster_summary.round(2))



    st.markdown("---")

    st.subheader("Cluster Interpretation")

    st.success("""
    ### 🎵 Cluster 0 - Calm / Acoustic Songs

    • High Acousticness (0.75)

    • Low Energy (0.31)

    • Low Danceability (0.49)

    • Moderate Tempo (112 BPM)

    • Suitable for relaxing, acoustic and soft music.
    """)

    st.info("""
    ### 🎵 Cluster 1 - Energetic / Party Songs

    • Highest Energy (0.69)

    • High Danceability (0.63)

    • Highest Valence (0.67)

    • Fastest Tempo (125 BPM)

    • Suitable for workout, dance and party playlists.
    """)

    st.warning("""
    ### 🎵 Cluster 2 - Spoken / Live Performance Songs

    • Very High Speechiness (0.83)

    • Highest Liveness (0.44)

    • Lowest Instrumentalness (0.001)

    • Shortest Duration (~98 sec)

    • Represents spoken-word, rap, live recordings or podcast-like audio.
    """)


elif page == "⭐ Top Songs":

    st.title("⭐ Top Songs by Cluster")

    cluster = st.selectbox(
        "Select a Cluster",
        sorted(df["Cluster"].unique())
    )

    top_songs = (
        df[df["Cluster"] == cluster]
        .sort_values(by="popularity_songs", ascending=False)
        [["name_song", "name_artists", "popularity_songs"]]
        .head(10)
    )

    st.subheader(f"Top 10 Songs in Cluster {cluster}")

    st.dataframe(top_songs, use_container_width=True)

elif page == "🔍 Song Search":

    st.title("🔍 Search a Song")

    song_name = st.text_input("Enter Song Name")

    if song_name:

        result = df[df["name_song"].str.contains(song_name,case=False,na=False)]

        if result.empty:

            st.error("Song not found in the dataset.")

        else:

            song = result.iloc[0]

            st.subheader("Song Details")

            st.write(f"**Song Name:** {song['name_song']}")
            st.write(f"**Artist:** {song['name_artists']}")
            st.write(f"**Cluster:** {song['Cluster']}")
            st.write(f"**Popularity:** {song['popularity_songs']}")

            st.markdown("---")

            st.subheader("Audio Features")

            st.write(f"🎵 Danceability : {song['danceability']:.2f}")
            st.write(f"⚡ Energy : {song['energy']:.2f}")
            st.write(f"🎤 Speechiness : {song['speechiness']:.2f}")
            st.write(f"🎸 Acousticness : {song['acousticness']:.2f}")
            st.write(f"🥁 Instrumentalness : {song['instrumentalness']:.2f}")
            st.write(f"❤️ Valence : {song['valence']:.2f}")
            st.write(f"🎼 Tempo : {song['tempo']:.2f}")

            st.markdown("---")

            st.subheader("Recommended Similar Songs")

            recommendations = (
                df[
                    (df["Cluster"] == song["Cluster"]) &
                    (df["name_song"] != song["name_song"])
                ]
                .sort_values(by="popularity_songs", ascending=False)
                [["name_song", "name_artists", "popularity_songs"]]
                .head(5)
            )

            st.dataframe(recommendations, use_container_width=True)    