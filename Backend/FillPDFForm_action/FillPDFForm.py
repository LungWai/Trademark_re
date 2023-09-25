import fitz
import json

PAGE_FIELD_MAPPINGS = [
  {},
  {
    "1.name": "Text Field0",
    "1.address.flat": "Text Field1",
    "1.address.street": "Text Field2",
    "1.address.country": "Combo Box2",
    "1.address.state": "Text Field689",
    "1.type": "Check Box0",
    "1.country": "Text Field688",
    "1.state": "Text Field687",
    "2.name": "Text Field6",
    "2.address.flat": "Text Field7",
    "2.address.street": "Text Field8",
    "2.telephone": "Text Field9",
    "2.fax": "Text Field10",
    "2.reference": "Text Field11"
  },
  {
    "3.name": "Text Field12",
    "3.address.flat": "Text Field13",
    "3.address.street": "Text Field14",
    "3.address.country": "Combo Box9",
    "3.telephone": "Text Field15",
    "3.fax": "Text Field16",
    "3.reference": "Text Field17"
  },
  {
    "4": "Push Button0",
    "4.details": "Text Field18",
    "4.series": "Combo Box3",
  },
  {
    "5.language": "Text Field20",
    "5.translation.letters": "Text Field21",
    "5.translation.transliteration1": "Text Field22",
    "5.translation.transliteration2": "Text Field23",
    "6.a": "Check Box3",
    "6.colour": "Text Field24",
    "6.b": "Check Box4",
    "6.3dshape": "Text Field25",
    "6.c": "Check Box5",
    "6.d": "Check Box6",
    "6.e": "Check Box7",
    "6.others": "Text Field26"
  },
  {
    "7.1": "Combo Box4",
    "7.specs1": "Text Field32",
    "7.2": "Combo Box5",
    "7.specs2": "Text Field33"
  },
  {
    "7.3": "Combo Box6",
    "7.specs3": "Text Field34",
    "7.4": "Combo Box7",
    "7.specs4": "Text Field35",
    "7.total": "Combo Box8"
  },
  {
    "8.date": "Text Field36",
    "8.countries": "Text Field3",
    "8.applications": "Text Field38",
    "8.details": "Text Field39",
    "9.certification": "Check Box8",
    "9.collective": "Check Box8",
    "9.defensive": "Check Box8",
    "10": "Text Field40"
  },
  {
    "11.signature": "Text Field41",
    "11.signatory": "Text Field42",
    "11.capcity": "Text Field43",
    "11.date": "Text Field44",
    "12": "Text Field45"
  }
]


"""
Sample data for testing

"""
# PREV_BLOCK_DATA = {
#   "1.name": "ABCC Company Limited",
#   "1.address.flat": "Suite 1223, Happy Plaza,",
#   "1.address.street": "121 Des Voeux Road Central,",
#   "1.address.state": "Hong Kong",
#   "1.type": "2",
#   "1.country": "UNITED STATES OF AMERICA",
#   "1.state": "NA",
#   "2.name": "Lee & Co.",
#   "2.address.flat": "Suite 507, Delight Plaza,",
#   "2.address.street": "130 Des Voeux Road,",
#   "2.telephone": "21234567",
#   "2.fax": "23216547",
#   "2.reference": "TM/0507",
#   "3.name": "Lee & Co.",
#   "3.address.flat": "Suite 507, Delight Plaza,",
#   "3.address.street": "130 Des Voeux Road,",
#   "3.address.country": "HONG KONG",
#   "3.telephone": "21234567",
#   "3.fax": "23216547",
#   "3.reference": "TM/0507",
#   ####
#   "4": "DIsneyland",
#   "4.details": "Disneyland",
#   "5.language": "Symbolic",
#   "5.translation.letters": "τ μ",
#   "5.translation.transliteration1": "T",
#   "5.translation.transliteration2": "M",
#   "6.a": True,
#   "6.colour": "Color combination is part of the mark",
#   "6.e": True,
#   "6.others": "Stylized letters are part of the mark",
#   "7.1": "27",
#   "7.specs1": "Software",
#   "7.2": "23",
#   "7.specs2": "Services",
#   "7.total": "2",
#   "8.date": "01-01-2020",
#   "9.certification": "1",
#   "10": "The logo shall be our exclusive intellectual property",
#   "11.signature": "John",
#   "11.signatory": "John Doe",
#   "11.capcity": "Founder",
#   "11.date": "03-05-2024",
#   "12": "3"
# }


def populate_fields(fields, responses = {}):
  """
  Populates the fields dictionary with the field names and values from the responses dictionary.
  """
  for field in fields:
    value = responses.get(field.field_name)
    
    if not value:
      continue
    field_type = field.field_type_string 
       
    if field_type == "CheckBox":
      if (type(value) is not bool) and (value in field.button_states()['normal']):
        value = True
      else:
        field.field_value = value
    elif field_type == "ComboBox" and ((type(value) is int) or value.isnumeric()):      
      opt = field.choice_values[int(value)]            
      if type(opt) is not str:        
        value = opt[-1]
      field.field_value = value      
    else:
      field.field_value = value
    field.update()


"""
Generates a PDF file based on the provided data.

Args:
  data (dict): A dictionary containing the data to be used in generating the PDF.
  filename (str): The name of the output PDF file.
"""
def generate_pdf(data = {}, filename = "Backend/FillPDFForm_action/Report.pdf"):
  
  #global Responses

  # Open the form template
  pdf = fitz.open("Backend/FillPDFForm_action/Filing-FormT2_clean.pdf")

  # Update form field values
  # responses = Responses | data
  responses = data
  for i, mappings in enumerate(PAGE_FIELD_MAPPINGS):
    print(f"Processing page {i}")
    page = pdf[i]
    # Get the fields on the page
    fields_data = {}
    for key, field_name in mappings.items():
      # Populate the fields data from responses
      if key in responses.keys():
        fields_data[field_name] = responses[key]
    # If there are responses for this page, fill the values
    if bool(fields_data):
      populate_fields(page.widgets(), fields_data)

  # Populate images for image fields
  image_fields = {
    # page#: fields
    3: ["4"], # Trademark
    8: ["11.signature"] # Signature
  }
  for i, fields in image_fields.items():
    page = pdf[i]
    for field in fields:
      # Obtain the field value
      value = responses.get(field)
      if not value:
        continue
      # Build an image from the text
      image = build_image(responses[field])
      # Obtain the field name in PDF
      field_name = PAGE_FIELD_MAPPINGS[i][field]
      # Get the bounding box for the field
      bbox = None
      for widget in page.widgets():
        if widget.field_name == field_name:
          bbox = widget.rect
          widget.field_value = False
          widget.update()
          break
      if bbox:
        dx = bbox.width // 10
        dy = bbox.height // 10
        page.insert_image((bbox.x0+dx, bbox.y0+dy, bbox.x1-dx, bbox.y1-dy), filename=image)

  # Write the output pdf
  #pdf.save(filename, clean=True, deflate=True)
  pdf.save(filename, clean=True)


def build_image(text):
  """
  Builds an image from the provided text.
  """
  from PIL import Image, ImageDraw, ImageFont

  # Load the font specifying file and size
  font = ImageFont.truetype("Backend/FillPDFForm_action/BungeeSpice-Regular.ttf", 50)

  # Create a blank image with a white background
  l, t, r, b = font.getbbox(text)
  width, height = r-l, b-t
  logo_image = Image.new("RGB", (width, height), "white")

  # Draw the text on the image
  draw = ImageDraw.Draw(logo_image)
  text_position = ((width - draw.textlength(text, font=font)) // 2, 0)
  draw.text(text_position, text, font=font, fill="blue")

  # Save the image and return the path
  filepath = f"Backend/FillPDFForm_action/{text}.png"
  logo_image.save(filepath)
  return filepath


def DataAndForm_assignment(json_string_API_FROM_UI ):

  #Sample input
  """
  Here is sample JSON string obtained from UI.

  Format:
    name_of_JSON_variable : sample_value
  
  """
  #print(json_string_API_FROM_UI)
  #json_string_API_FROM_UI = '{"ui_applicant_name_1" : "ABCC Company Limited","ui_applicant_flat_address_1" : "Suite 1223 Happy Plaza", "ui_applicant_street_address_1" : "121 Des Voeux Road Central", "ui_applicant_state_address_1" : "Hong Kong", "ui_applicant_type_1" : "2", "ui_incorporation_country_1" : "UNITED STATES OF AMERICA", "ui_incorporation_state_1" : "NA", "ui_correspondence_name_2" : "Lee & Co", "ui_correspondence_flat_address_2" : "Suite 507 Delight Plaza", "ui_correspondence_street_address_2" : "130 Des Voeux Road", "ui_correspondence_telephone_2" : "21234567", "ui_correspondence_fax_2" : "23216547", "ui_correspondence_reference_2" : "TM/0507", "ui_agent_name_3" : "Lee & Co", "ui_agentr_flat_address_3" : "Suite 507 Delight Plaza", "ui_agent_street_address_3" : "130 Des Voeux Road", "ui_agent_country_address_3" : "HONG KONG", "ui_agent_telephone_3" : "21234567", "ui_agent_fax_3" : "23216547", "ui_agent_reference_3" : "TM/0507", "ui_language_5" : "Symbolic", "ui_translation_letters_5" : "wew", "ui_translation_transliteration1_5" : "T", "ui_translation_transliteration2_5" : "M", "ui_checkBox_color_6" : "True", "ui_color_6" : "Color combination is part of the mark", "ui_checkBox_shape_6" : "", "ui_shape_6" : "", "ui_checkBox_sound_6" : "", "ui_checkBox_smell_6" : "", "ui_checkBox_others_6" : "True", "ui_others_6" : "Stylized letters are part of the mark", "ui_convention_date_8" : "01-01-2020", "ui_convention_countries_8" : "", "ui_convention_applications_8" : "", "ui_convention_details_8" : "", "ui_checkbox_certification_9" : "True", "ui_checkbox_collective_9" : "", "ui_checkbox_defensive_9" : "", "ui_disclaimer_10" : "The logo shall be our exclusive intellectual property", "ui_confirmation_signatory_11" : "John Doe", "ui_confirmation_capacity_11" : "Founder", "ui_confirmation_date_11" : "03-05-2024"}'
  data=json.loads(json_string_API_FROM_UI)

  """
  Here are data required from previous blocks for:
  - Section 4: Trade Mark Text for logo generation
  - Section 7: Class & SPecification pairs

  with hardcode value

  """
  # Section 4 
  previous_block_trademark_text_logo_4 = "Disneyland"  #Path
  previous_block_trademark_4 = "Disneyland" #Path

  # Section 7
  previous_block_class1_7 = "45"
  previous_block_specification1_7 = "Specification1 sample"

  previous_block_class2_7 = "42" 
  previous_block_specification2_7 = "Specification2 sample" 

  # for completeness, keep for minimizing the changes in program requred 
  total_7 = "" 
  confirmation_signature_11 = "" 
  total_attachment_12 = "" 


  """ 
  Putting variables into Form

  """
  PREV_BLOCK_DATA = {
    "1.name": data["applicant_name_1"],
    "1.address.flat": data["applicant_flat_address_1"],
    "1.address.street": data["applicant_street_address_1"],
    "1.address.state": data["applicant_state_address_1"],
    "1.type": data["applicant_type_1"],
    "1.country": data["incorporation_country_1"],
    "1.state": data["incorporation_state_1"],
    "2.name": data["correspondence_name_2"],
    "2.address.flat": data["correspondence_flat_address_2"],
    "2.address.street": data["correspondence_street_address_2"],
    "2.telephone": data["correspondence_telephone_2"],
    "2.fax": data["correspondence_fax_2"],
    "2.reference": data["correspondence_reference_2"],
    "3.name": data["agent_name_3"],
    "3.address.flat": data["agent_flat_address_3"],
    "3.address.street": data["agent_street_address_3"],
    "3.address.country": data["agent_country_address_3"],
    "3.telephone": data["agent_telephone_3"],
    "3.fax": data["agent_fax_3"],
    "3.reference": data["agent_reference_3"],
    ####
    "4": previous_block_trademark_text_logo_4,
    "4.details": previous_block_trademark_4,
    "5.language": data["language_5"],
    "5.translation.letters": data["translation_letters_5"],
    "5.translation.transliteration1": data["translation_transliteration1_5"],
    "5.translation.transliteration2": data["translation_transliteration2_5"],
    "6.a": data["checkBox_color_6"],
    "6.colour": data["color_6"],
    "6.e": data["checkBox_others_6"],
    "6.others": data["others_6"],
    "7.1": previous_block_class1_7,
    "7.specs1": previous_block_specification1_7,
    "7.2": previous_block_class2_7,
    "7.specs2": previous_block_specification2_7,
    "7.total": total_7,
    "8.date": data["convention_date_8"],
    "9.certification": data["checkbox_certification_9"],
    "10": data["disclaimer_10"],
    "11.signature": confirmation_signature_11,
    "11.signatory": data["confirmation_signatory_11"],
    "11.capcity": data["confirmation_capacity_11"],
    "11.date": data["confirmation_date_11"],
    "12": total_attachment_12
  }
  
  # Generate the PDF
  generate_pdf(PREV_BLOCK_DATA)

#if __name__ == "__main__":
#  DataAndForm_assignment()


