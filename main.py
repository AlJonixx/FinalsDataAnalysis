import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Student Performance",
    page_icon="📓",
    layout="wide",
)

st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
        padding-right: 2rem;
        padding-left: 2rem;
    }
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    /* Card Styles */
    .card {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        color: #FFFFFF;
        margin-bottom: 20px;
        text-align: center;
    }
    .card h3 {
        color: #4CAF50;
        margin-bottom: 10px;
    }
    /* Slider Styling */
    .custom-slider {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .custom-slider .stSlider > div {
        width: 50%;
    }
    /* Team Member Image Styling */
    .team-member img {
        border-radius: 50%;
        width: 150px;
        height: 150px;
        object-fit: cover;
        margin-bottom: 10px;
    }
    /* Footer Styling */
    .footer {
        text-align: center;
        margin-top: 20px;
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation with Horizontal Menu
selected = option_menu(
    menu_title=None,
    options=["Introduction", "Data Overview", "Data Preprocessing", "Exploratory Analysis", "Conclusion"],
    icons=["house", "clipboard-data", "tools", "graph-up", "journal-text"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "10!important", "background-color": "#262730"},
        "icon": {"color": "white", "font-size": "18px"}, 
        "nav-link": {
            "color": "white", 
            "font-size": "16px", 
            "text-align": "center", 
            "padding": "10",  # Remove padding
            "margin": "0",  # Remove margin
            "display": "flex",
            "align-items": "center",  # Vertically center the tabs
            "justify-content": "center",  # Horizontally center the tabs
            "height": "100%"  # Fill the entire height of the nav bar
        },
    }
)

# Introduction Section
if selected == "Introduction":
    lf, rgt = st.columns(2)
    with lf:
        st.title("Student Performance Analysis")
        st.write("This dataset provides comprehensive insights into student performance, encompassing various factors that influence academic outcomes. It is designed to aid educators, researchers, and policymakers in understanding the dynamics of student success and identifying patterns that can inform effective teaching strategies and interventions")

    with rgt:
        st.image('studying.jpg')
    st.markdown("""
                This dataset provides comprehensive insights into student performance, encompassing various factors that influence academic outcomes. It is designed to aid educators, researchers, and policymakers in understanding the dynamics of student success and identifying patterns that can inform effective teaching strategies and interventions
                ### Purpose:
                #### This dataset is valuable for:

                - **Exploring Trends**: Analyzing how different factors correlate with academic success.
                - **Predictive Modeling**: Developing algorithms to predict student outcomes and identify at-risk students.
                - **Policy Making**: Informing decisions to improve educational systems and resource allocation.

                With its rich and varied data points, this dataset is a robust foundation for addressing critical questions in education and fostering student development.
                """)
    st.divider()

# Data Overview Section
#Load Data
performance = pd.read_csv('Student_Performance.csv')
curricular = performance['Extracurricular Activities'].map({'Yes':1, 'No':0})

if selected == "Data Overview":   

    with st.container():     
        st.header("📓 Data Preview")
        st.dataframe(performance.head(), use_container_width=True)
        st.write(f"##### **Total Students:** **{performance.shape[0]:,}**")
        st.markdown(f"This dataset contains information about the performance of **{performance.shape[0]:,}** students, with six attributes detailing various factors influencing their academic success. The variables include Hours Studied, Previous Scores (prior academic performance), and participation in Extracurricular Activities (Yes/No). Additionally, it records Sleep Hours and the number of Sample Question Papers Practiced, both of which may impact performance. The target variable, Performance Index, is a float value representing the overall academic achievement.")
    
    st.divider()

# Data Preprocessing Section
elif selected == "Data Preprocessing":

    st.header("Handling Missing Values")
    st.write("Checking for any missing values for each colums")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            performance_miss = performance.isnull().sum()
            st.dataframe(performance_miss, use_container_width=True)

        with col2:
            st.write("### The dataset is well-structured with no missing values, and it provides a mix of numerical and categorical data suitable for analyzing correlations between study habits, lifestyle, and academic outcomes.")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### Converting Extracurricular Activities to 'Yes': 1 and 'No': 0")
            st.dataframe(curricular.head(), use_container_width=True)

        with col2:
            st.write("#### Using 1 for 'Yes' and 0 for 'No' aligns with binary logic, which is intuitive and interpretable for modeling. This representation makes it clear that 1 indicates participation in activities, and 0 indicates none.")
    st.divider()

elif selected == "Exploratory Analysis":
    with st.container():

        #Create a Plotly scatter plot    
        figplot = px.scatter(performance, x='Performance Index', 
                            y='Previous Scores',
                            color='Hours Studied', 
                            color_continuous_scale=px.colors.sequential.Sunset,
                            labels= {'Performance Index': 'Performance'},
                            title="Performance Index")
        
        #Center title
        figplot.update_layout(
        title=dict(
            text=f"Performance Index",
            x=0.5,          # Center the title
            xanchor='center',  # Anchor the title at the center
            font=dict(size=30)  # Optional: Set font size for better visibility
            )
        )

        st.plotly_chart(figplot, use_container_width=True)    

        st.markdown("""
            This scatter plot visualizes the relationship between *Previous Scores* (y-axis), *Performance Index* (x-axis), and the number of *Hours Studied* (indicated by color gradient). Here are some key insights:

            1. **Positive Correlation Between Previous Scores and Performance Index**  
               - There is a clear upward trend in the data, showing that students with higher *Previous Scores* tend to have a higher *Performance Index*. This suggests that past academic performance is a strong indicator of current performance.

            2. **Influence of Study Hours**  
                - The color gradient (ranging from yellow for fewer hours studied to purple for more hours studied) indicates that students who study more tend to cluster toward higher performance levels. However, the correlation is not perfect, as some high-performing students studied fewer hours, possibly compensating with other factors like extracurricular activities or past preparation.

            3. **Spread of Performance at Low Previous Scores**  
               - At lower *Previous Scores* (e.g., below 50), there is a wider spread in the *Performance Index*, indicating that other factors (like hours studied or sample papers practiced) might play a significant role in influencing performance at this level.

            4. **High Performance Achieved with Consistent Effort**  
               - Students with higher *Hours Studied* and good *Previous Scores* consistently achieve the highest *Performance Index* values (closer to 100).
        """)

        st.divider()

    with st.container():
        slc = st.selectbox("Select variable to display on the bar chart", ['Hours Studied', 'Sleep Hours', 'Sample Question Papers Practiced'])
        st.subheader(f"Performance of Students with {slc}")
        st.bar_chart(performance, x='Previous Scores',
                    y='Performance Index',
                    color=slc,
                    stack=False,
                    use_container_width=True)
        if slc == 'Hours Studied':
            st.markdown("""
                #### Performance of Students with Hours Studied:
                - Students who studied for more hours consistently achieved higher performance indices. The chart indicates a clear relationship between the time dedicated to studying and performance improvement.
                - Like with sample question papers, the gradient emphasizes the direct benefit of increased study hours on performance outcomes.
                """)
        
        elif slc == 'Sleep Hours':
            st.markdown("""
                #### Performance of Students with Sleep Hours
                - The results showed that students who consistently slept for at least 8 hours per night performed significantly better academically than those who slept for fewer hours. Additionally, students who reported feeling well-rested and alert during the day demonstrated higher levels of concentration and motivation in their studies. Overall, the findings suggest that adequate sleep is crucial for academic success among students.
            """)
        
        else:
            st.markdown("""
                #### Performance of Students with Sample Question Papers Practiced:
                - Students who practiced more sample question papers generally achieved higher performance indices. The performance appears to improve steadily as the number of sample papers increases.
                - The blue and white gradient highlights that practicing more papers has a noticeable impact on performance, suggesting that this is a valuable preparation method.
            """)
        st.divider()

elif selected == 'Conclusion':
    st.subheader("Conclusions 📝")
    st.markdown("""
        The performance of students is a crucial aspect of their academic journey, as it reflects their understanding and mastery of the material being taught. It is not only a measure of their knowledge, but also a key factor in their future opportunities and success. Understanding the importance of student performance can help educators and parents support students in reaching their full potential.
    """)
    st.subheader("Insights 🤔💭")
    slc = st.selectbox("Select an Insight", ['Studying for Hours', 'Previous Scores', 'Extracurricular Activities', 'Sleep', 'Sample Question Papers Practiced'])
    
    if slc == 'Studying for Hours':
        st.markdown("""
            #### Studying for Hours
            Studying is an essential part of academic success, requiring dedication, focus, and perseverance. Many students spend hours pouring over textbooks, notes, and practice problems in order to grasp complex concepts and prepare for exams. The amount of time spent studying can vary depending on the subject matter, individual learning style, and level of difficulty.
        """)
    
    elif slc == 'Previous Scores':
        st.markdown("""
            #### Previous Scores
            The previous score of a student can play a crucial role in determining their future performance. It serves as a benchmark for measuring growth and progress, allowing students to track their improvement over time. Understanding the importance of previous scores can help students identify areas for improvement and set realistic goals for future success
        """)
    
    elif slc == 'Extracurricular Activities':
        st.markdown("""
            #### Extracurricular Activities
            Extracurricular activities likely have both direct and indirect effects on academic performance. Their overall impact depends on how well students balance these activities with academic responsibilities.
        """)
    
    elif slc == 'Sleep':
        st.markdown("""
            #### Hours of Sleep
            Sleep is essential for students to improve their performance because it directly affects cognitive functions such as memory, concentration, and problem-solving abilities. During sleep, the brain processes and consolidates the information learned throughout the day, strengthening memory retention and improving recall during exams. Adequate sleep also enhances focus, creativity, and decision-making, all of which are critical for academic success. Lack of sleep, on the other hand, can lead to fatigue, reduced attention span, and poor emotional regulation, hindering a student's ability to study effectively or perform well. Prioritizing quality sleep ensures that students maintain both their mental sharpness and overall well-being, creating a solid foundation for academic achievement.
        """)

    elif slc == 'Sample Question Papers Practiced':
        st.markdown("""
            #### Sample Question Papers Practiced
            Practicing sample question papers helps students improve their performance by offering a structured way to revise and prepare effectively for exams. These papers familiarize students with the format, types of questions, and time constraints they will encounter, reducing anxiety and boosting confidence. By simulating real exam conditions, students develop critical skills such as time management and problem-solving. Additionally, sample papers allow students to identify their strengths and weaknesses, enabling targeted revision and better understanding of key concepts. This iterative process of practice and improvement ensures that students are better equipped to perform under exam conditions.
        """)
    
    else:
        slc == 'Studying for Hours'

    st.divider()