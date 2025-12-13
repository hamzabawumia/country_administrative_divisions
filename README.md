## Country Administrative Divisions

Administrative divisions (regions, districts, etc.) linked to countries.




First clone this app and install it into your project
it comes with two doctypes that are already linked to the erpnext countries doctype.

1. Admin Level 1 Province_Region_State(1)
    with the following fields:
    {
    "country_id", - links to country (erpnext country doctype)
    "province_region_state"
    }
    
2. Admin Division Level 2 Districts_County_City_Town(2)
    with the following fields:
    {
    "admin_division_level_1", - links to "Admin Level 1 Province_Region_State"(1)
    "district_county_city_town"
    }
    
so in your project, you only need to link to the above doctypes 
and everything will work smoothly.

you should create 3 fields in your new doctype

1. country - linked to erpnext "country" doctype
2. province_region_state - linked to "Admin Level 1 Province_Region_State" (1)
3. districts_county_city_town - linked to "Admin Division Level 2 Districts_County_City_Town"(2)

Naming conventions for the fields when creating your own fields:

Level_1
    Label = Province / Region / State
    name = province_region_state
    This links to = Admin Level 1 Province_Region_State

Level_2
    Label = District / County / City / Town
    name = districts_county_city_town
    This links to = Admin Division Level 2 Districts_County_City_Town
    
    
How to Implement the Selection Flow
with Dependent or Chained Dropdown List FOR DESK:

BEST TO USE THE FILTER ICON IN THE LINK FIELD ITSELF:
--------------------------------------------------------
Click the filter icon for the field you want. 
Build filter: ....

Operator: =

Value type: will be an Expression

example 
eval:doc.country  (note that there is no quotes around the value)


so you are going to have something like so:

[
  [<TargetDoctype>, <FieldInTargetDoctype>, <Operator>, <Value>]
  
  TargetDoctype is the doctype that will be filtered
  
  ["Admin Level 1 Province_Region_State", "country_id", "=", "eval:doc.country"]

]

[
  [<TargetDoctype>, <FieldInTargetDoctype>, <Operator>, <Value>]

  ["Admin Division Level 2 Districts_County_City_Town", "admin_division_level_1",
  "=","eval:doc.province_region_state"
  ]
]

    
#### License

mit
