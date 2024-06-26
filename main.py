from flask import Flask, request, send_file, jsonify
import pdfkit
import os
import tempfile

app = Flask(__name__)

@app.route('/generate_resume', methods=['POST'])
def generate_resume_endpoint():
    data = request.json
    
    # Preprocess data to handle missing fields and specific formatting
    full_name = data.get("Full Name", "")
    email = data.get("Email", "")
    date_of_birth = data.get("Date of Birth", "")
    gender = data.get("Gender", "")
    mobile_number = data.get("Mobile Number", "")
    alternate_number = data.get("Alternate Number", "")
    address = data.get("Address", "")
    pincode = data.get("Pincode", "")
    current_location = data.get("Current Location", "")
    sub_location = data.get("Sub Location", "")
    about_us = data.get("About Us", "")
    hobbies_interests = data.get("Hobbies & Interests", "")
    work_experience = data.get("Work Experience", [])
    education_details = data.get("Education Details", {})
    strengths = data.get("Strengths", [])
    achievements = data.get("Achievements", [])
    skills = data.get("Skills", [])
    languages = data.get("Languages", [])
    
    # Prepare the work experience, strengths, achievements, skills, and languages sections
    work_experience_html = "".join([f"""
        <div class='job'>
            <h6>{job['Company']}</h6>
            <p>{job['Designation']} ({job['Start Date']} - {job['End Date']})</p>
            <p>{job['Location']}</p>
            <ul>
                {''.join([f"<li>{responsibility}</li>" for responsibility in job['Responsibilities']])}
            </ul>
        </div>
    """ for job in work_experience])
    
    strengths_html = "".join([f"<li>{strength}</li>" for strength in strengths])
    achievements_html = "".join([f"<li>{achievement}</li>" for achievement in achievements])
    skills_html = "".join([f"<li>{skill}</li>" for skill in skills])
    languages_html = "".join([f"<li>{lang['Language']} ({lang['Proficiency']})</li>" for lang in languages])
    
    # Load the HTML template
    with open('resume_template.html', 'r') as file:
        html_template = file.read()
    
    # Insert data into the HTML template
    html_content = html_template.format(
        full_name=full_name,
        email=email,
        date_of_birth=date_of_birth,
        gender=gender,
        mobile_number=mobile_number,
        alternate_number=alternate_number,
        address=address,
        pincode=pincode,
        current_location=current_location,
        sub_location=sub_location,
        about_us=about_us,
        hobbies_interests=hobbies_interests,
        work_experience=work_experience_html,
        education_qualification=education_details.get("Highest Qualification", ""),
        education_institute=education_details.get("Institute", ""),
        education_graduation_year=education_details.get("Graduation Year", ""),
        strengths=strengths_html,
        achievements=achievements_html,
        skills=skills_html,
        languages=languages_html,
        linkedin_profile=f"Linkedin.com/in/{full_name.replace(' ', '').lower()}"
    )
    
    # Save HTML content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html_file:
        tmp_html_file.write(html_content.encode('utf-8'))
        tmp_html_path = tmp_html_file.name
    
    # Define PDF output path
    tmp_pdf_path = tempfile.mktemp(suffix=".pdf")
    
    # Convert HTML to PDF

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')


    pdfkit.from_file(tmp_html_path, tmp_pdf_path, configuration=config, options={
        'enable-local-file-access': ''
    })
    
    # Clean up temporary HTML file
    os.remove(tmp_html_path)
    
    # Send the PDF file as a response
    return send_file(tmp_pdf_path, as_attachment=True, download_name="resume.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
