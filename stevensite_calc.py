#stevensite solubility product is below from a given paper

#Given:
#logK = 25.45 @ 25C

#(Si_4.00, Mg_2.9, O_10, (OH)_2, Ca_0.1) + 6H+ + 4H20 = 4H4SiO4 + 2.9Mg++ +  0.1Ca++)

#Ksp = (H4SiO4 ** 4) * (Mg ** 2.9) * (Ca ** 0.1) / ([H] ** 6)
#regarding the data set, Si is the limiting element for H4SiO4

#necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#load data, original df
df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/Data/metadata_ioncomp.csv')

#extracting columns
Mg = df['Magnesium (Mg)'].to_numpy()
Ca = df['Calcium (Ca)'].to_numpy()
H4SiO4 = df['Silicon (Si)'].to_numpy()  # ssuming silicon column represents H4SiO4
df['Date'] = pd.to_datetime(df['Sample Date'], format='%m/%d/%y')
temp = df['Temperature (C)'].to_numpy()

#scatter plot, comparing SI values
def plot_SI_scatter():
    df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/github/CSV Data/Stevensite_SI_phrqc.csv')

    df['Sample Type'] = df['Sample Type'].str.strip()

    colors = {
        'Inactive Pore Water': 'b',
        'Active Pore Water': 'r',
        'Surface Water': 'g',
        'Groundwater': 'y'
    }

    custom_labels = {
        'Inactive Pore Water': 'Inactive (PW)',
        'Active Pore Water': 'Active (PW)',
        'Surface Water': 'Boundary Lake',
        'Groundwater': 'Groundwater'
    }

    plt.figure(figsize=(10, 6))


    for sample_type, group in df.groupby('Sample Type'):
        label = custom_labels.get(sample_type, sample_type)
        plt.scatter([sample_type] * len(group), group['si_stevensite'],
                    label=label,
                    color=colors.get(sample_type, 'gray'), 
                    edgecolor='k')

    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, label='Equilibrium')
    plt.xlabel('Sample Type', fontweight='bold')
    plt.ylabel('SI (stevensite)', fontweight='bold')
    plt.title('SI of stevensite by Sample Type', fontweight='bold')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#box plot, comparing SI values to sample type
def plot_SI_boxplot():
    df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper'
    '/github/CSV Data/Stevensite_SI_phrqc.csv')

    df['Sample Type'] = df['Location ID'].str.strip()

    #filtering out rows where 'Location ID' is 'Undisclosed Porewater'
    df = df[df['Sample Type'] != 'Undisclosed Porewater']

    #displaying the number of data points used for the plot
    print(f"Number of data points used for the plot: {len(df)}")

    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(data=df, x='Sample Type', y='si_stevensite', palette='pastel')
    
    medians = df.groupby('Sample Type')['si_stevensite'].median()
    xticks = ax.get_xticks()
    
    for tick, label in zip(xticks, ax.get_xticklabels()):
        sample_type = label.get_text()
        median_value = medians[sample_type]
        ax.text(
            tick, median_value - 0.4,
            f'{median_value:.2f}',
            ha='center',
            va='bottom',
            fontsize=8,
            color='black',
            family='serif',
            style='italic'
        )

    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, label='Equilibrium')
    plt.title('SI of Stevensite by Sample Type', fontweight='bold')
    plt.ylabel('SI (Stevensite)', fontweight='bold')
    plt.xlabel('Sample Type', fontweight='bold')
    plt.xticks(rotation=45)
    plt.legend(loc='lower right', title='*Median values shown', fontsize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_facecolor('lightgrey')
    plt.gcf().patch.set_facecolor('white')
    plt.tight_layout()
    plt.show()

def plot_SI_MgSi_scatter():
    df = pd.read_csv('/Users/finleydavis/Desktop/Spring 25 Courses/Aqueous Geochem/Final Paper/github/CSV Data/Mg:Si_calc.csv')
    
    Mg_Si = df['Mg/Si Ratio'].to_numpy()
    SI = df['si_stevensite'].to_numpy()
    locations = df['Location ID'].astype(str).to_numpy()
    
    for i in range(len(locations)):
        if locations[i] == 'nan':
            locations[i] = 'Groundwater'
        else:
            locations[i] = locations[i].strip()


    unique_locations = np.unique(locations)
    cmap = plt.cm.get_cmap('tab20', len(unique_locations))
    colors = cmap(np.arange(len(unique_locations)))

    plt.figure(figsize=(10, 6))

    for i, location in enumerate(unique_locations):
        loc_mask = locations == location
        plt.scatter(Mg_Si[loc_mask], SI[loc_mask], color=colors[i], edgecolor='k', label=location)

    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, label='Equilibrium')
    plt.xlabel('Mg/Si Ratio', fontweight='bold')
    plt.ylabel('Saturation Index (Stevensite)', fontweight='bold')
    plt.title('Stevensite Saturation Index vs. Mg/Si Ratio', fontweight='bold')
    plt.legend(title='Location ID', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    
#plot_SI_scatter()
#plot_SI_boxplot()
plot_SI_MgSi_scatter()