
import makereadmes as mr

# Settings
lang_list = ["ES", "EN"]  # Available: "ES", "EN"
order_by = "Country"  # Available: "Country"

# Make main and web csv files
df = mr.makecsv()

# Create localized readme's
mr.create_localised_readme(lang_list,order_by, df)

# Create main readme.md
mr.create_main_readme()


