import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
 
# ------------- Page Config -------------
st.set_page_config(page_title="User Insights", page_icon="🚗", layout="wide")
 
# ------------- Sidebar Inputs -------------
st.sidebar.image("logo.png", width=200)
 
st.sidebar.markdown("## 🧾 User Details")
 
country = st.sidebar.selectbox("🌍 Select Country", ["USA", "China"])
age = st.sidebar.number_input("🎂 Enter Age", min_value=1, max_value=100, value=30)
gender = st.sidebar.selectbox("⚧️ Select Gender", ["Male", "Female"])
brand = st.sidebar.selectbox("🚘 Select Brand", ["Jaguar", "Defender", "Discovery", "Land Rover"])
source = st.sidebar.selectbox("Select Source", ["GCI", "NPS", "TGW"], index = 0)


submit = st.sidebar.button("🚀 Submit")

# ------------- Load Temperature & Problems Data -------------
temperature_df = pd.read_csv("min_max_temp_data.csv")
# problems_df = pd.read_csv("problems_data.csv")
 
# ------------- Function to Load data from CSV -------------
def load_height_weight(country, gender):
    country = country.lower()
    gender = gender.lower()
   
    height_file = f"{country}_{gender}_Height.csv"
    weight_file = f"{country}_{gender}_Weight.csv"
   
    height_df = pd.read_csv(height_file, skiprows=1)
    weight_df = pd.read_csv(weight_file, skiprows=1)
   
    print(weight_df)
    height = float(height_df.iloc[:, 9 if country == "USA" else 10].mean())   #mean
    weight = float(weight_df.iloc[:, 9 if country == "USA" else 10].mean())   #mean
    
    print(weight)
    return height, weight
 
def load_height_csv(country, gender):
    country = country.lower()
    gender = gender.lower()
    height_file = f"{country}_{gender}_Height.csv"
   
    height_df = pd.read_csv(height_file, skiprows=1)    
    return height_df

def load_weight_csv(country, gender):
    country = country.lower()
    gender = gender.lower()
    weight_file = f"{country}_{gender}_Weight.csv"
   
    weight_df = pd.read_csv(weight_file, encoding='unicode_escape', on_bad_lines='skip',skiprows=1)    
    return weight_df

def load_data_csv(country,source):
    country = country.lower()
    source = source.lower()
    data_file = f"{source}_{country}.csv"
    # st.write(data_file)

    data_frame = pd.read_csv(data_file, encoding='unicode_escape', on_bad_lines='skip') 
    return data_frame
 
# ------------- Main Output -------------
if submit:
    
    col1, col2 = st.columns(2)
 
    with col1:
        height_data = load_height_csv(country, gender)
        weight_data = load_weight_csv(country, gender)
       
        # Extract relevant columns for plotting
        age_groups = height_data.iloc[:, 0]
        mean_height = height_data.iloc[:, 2]
        mean_weight = weight_data.iloc[:, 2]
        # Plotting the temperature data
        st.markdown("### 📊 Weather Data")
        country_data = temperature_df[temperature_df["Country"] == country]
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size
        ax.plot(country_data["Month"], country_data["Max_Tdry"], label="Max Temperature (°C)", marker='o')
        ax.plot(country_data["Month"], country_data["Min_Tdry"], label="Min Temperature (°C)", marker='o')
        ax.set_xlabel("Month")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title(f"Monthly Temperature Data for {country}")
        ax.legend()
 
        # Rotate x-axis labels to vertical
        plt.xticks(rotation=90)
 
        st.pyplot(fig)
 
        # Plotting Height Graph
 
        st.markdown("### 🔥 Anthropometric Data")
        try:
            height, weight = load_height_weight(country, gender)
            if gender == 'Male':
                BMR = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                BMR = 10 * weight + 6.25 * height - 5 * age - 161
            st.markdown(f"**Height:** {height} cm | **Weight:** {weight} kg")
            st.markdown(f"**Predicted BMR:** {round(BMR, 2)} kcal/day")
        except Exception as e:
            st.markdown(f"Error loading height/weight data: {e}")
 
 
 
       
        # Plotting the height and weight data
       
        # Lambda function to calculate median age
        median_age = lambda ages: (int(ages.split(' ')[0]) + int(ages.split(' ')[-1])) / 2 if ' ' in ages else 90
       
        # Plotting the data
        fig, ax1 = plt.subplots(figsize=(10, 6))  # Adjust figure size
        if gender == 'Male':
            color = 'tab:red'
            ax1.set_xlabel('Age Group')
            ax1.set_ylabel('BMR', color=color)
            ax1.plot(age_groups, 10 * mean_weight + 6.25 * mean_height - 5 * median_age(age_groups) + 5, color=color, marker='o', label='Mean Height')
            ax1.tick_params(axis='y', labelcolor=color)
        else:
            color = 'tab:red'
            ax1.set_xlabel('Age Group')
            ax1.set_ylabel('BMR', color=color)
            ax1.plot(age_groups, 10 * mean_weight + 6.25 * mean_height - 5 * median_age(age_groups) - 161, color=color, marker='o', label='Mean Height')
            ax1.tick_params(axis='y', labelcolor=color)
 
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title('BMR by Age Group')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        
        st.markdown("### 🔥 Height Graph")

        fifty_percentile_height = height_data.iloc[:, 9 if country == "USA" else 10]
        # print(fifty_percentile_height)
        fig, ax1 = plt.subplots(figsize=(10, 6))  # Adjust figure size
        color = 'tab:red'
        ax1.set_xlabel('Age Group')
        ax1.set_ylabel('BMR', color=color)
        ax1.plot(age_groups,fifty_percentile_height, color=color, marker='o', label='Mean Height')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_ylim(min(fifty_percentile_height) * 0.9, max(fifty_percentile_height) *1.05 ) 
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title('Height by Age Group')
        plt.xticks(rotation=90)
        st.pyplot(fig)
 
        # Plottting Weight Graph
 
        st.markdown("### 🔥 Weight Graph")
        fifty_percentile_weight=weight_data.iloc[:, 9 if country == "USA" else 10]
        print(fifty_percentile_weight)
        fig, ax1 = plt.subplots(figsize=(10, 6))  # Adjust figure size
        color = 'tab:red'
        ax1.set_xlabel('Age Group')
        ax1.set_ylabel('BMR', color=color)
        ax1.plot(age_groups,fifty_percentile_weight, color=color, marker='o', label='Mean weight')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_ylim(min(fifty_percentile_weight) * 0.9, max(fifty_percentile_weight) *1.05 ) 
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title('Weight by Age Group')
        plt.xticks(rotation=90)
        st.pyplot(fig)
 
    with col2:
        st.markdown("### ❗ User Insights")
        
        problems_df = load_data_csv(country,source)
        # Filter data where Country is equal to 'Country'
        # filtered_df = problems_df[problems_df['Country'] == {country}]
        
        
        
        # Create a bar graph
        plt.figure(figsize=(10,6))
        
        count_by_cluster = problems_df["Cluster ID"].value_counts().sort_index()
        unique_cluster_ids = problems_df["Cluster ID"].unique()

        bars = plt.bar(problems_df["Cluster ID"].unique(), count_by_cluster.values, color='skyblue')
        plt.xlabel("Prevalence")
        plt.ylabel("Number of Issues")
        
        plt.xticks(problems_df["Cluster ID"])

        # Add labels to each bar
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center', va='bottom')
        
        # Display the plot
        st.pyplot(plt)
        
        
        
        # Create a single box to display all issues
        issues_text = ""
        
        for cluster_id in unique_cluster_ids:
            # st.write(f'Issues for Cluster ID {cluster_id}:')
            filtered_issues = problems_df[problems_df["Cluster ID"] == cluster_id]['Issue']
            if not filtered_issues.empty:
                first_issue = filtered_issues.iloc[0]
                issues_text += f"\n\n **Issue {cluster_id}** : {first_issue}" 
            issues_text += f"\n"
                
        st.markdown(f"""<div style="border: 1px solid #ccc; padding: 10px; margin: 10px 10px; border-radius: 5px;"> {issues_text} </div>""", unsafe_allow_html=True)