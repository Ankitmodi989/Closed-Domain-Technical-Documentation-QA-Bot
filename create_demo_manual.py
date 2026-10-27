from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUTPUT = Path("output/pdf/Sample_University_Student_IT_Services_Manual.pdf")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#18324B")
BLUE = colors.HexColor("#2A6F97")
PALE = colors.HexColor("#EAF2F7")
INK = colors.HexColor("#263442")
MUTED = colors.HexColor("#5B6B78")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27, leading=33, textColor=NAVY, alignment=TA_LEFT, spaceAfter=16))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=13, leading=19, textColor=MUTED, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="SectionTitle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle(name="SubTitle", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=BLUE, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyText2", parent=styles["BodyText"], fontSize=9.5, leading=14, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="SmallNote", parent=styles["BodyText"], fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=9, leading=13, textColor=NAVY))
styles.add(ParagraphStyle(name="CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=BLUE, spaceAfter=14))


def para(text, style="BodyText2"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph(f"&bull;&nbsp;&nbsp;{text}", styles["BodyText2"])


def callout(text):
    table = Table([[para(text, "Callout")]], colWidths=[6.45 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C7DCE8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = letter
    if doc.page > 1:
        canvas.setFillColor(BLUE)
        canvas.rect(0, height - 0.16 * inch, width, 0.16 * inch, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(0.75 * inch, height - 0.42 * inch, "SAMPLE UNIVERSITY  /  STUDENT IT SERVICES")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.75 * inch, 0.42 * inch, "SYNTHETIC PROJECT SAMPLE - NOT OFFICIAL UNIVERSITY POLICY")
        canvas.drawRightString(width - 0.75 * inch, 0.42 * inch, f"{doc.page}")
        canvas.setStrokeColor(colors.HexColor("#D6E0E7"))
        canvas.line(0.75 * inch, 0.58 * inch, width - 0.75 * inch, 0.58 * inch)
    canvas.restoreState()


story = []

# Cover
story.extend([Spacer(1, 0.75 * inch), para("STUDENT TECHNOLOGY GUIDE  /  VERSION 1.0", "CoverKicker"),
              para("Student IT<br/>Services Manual", "CoverTitle"),
              para("A quick reference for accounts, campus Wi-Fi, remote access, learning systems, printing, and support.", "CoverSub"),
              Spacer(1, 0.42 * inch), callout("<b>Demo document:</b> Sample University is fictional. This manual was created solely to demonstrate a closed-domain question-answering project. It is not an official policy and must not be used for real account or security decisions."),
              Spacer(1, 0.35 * inch), para("IN THIS GUIDE", "SubTitle"),
              bullet("Student account and password reset"), bullet("Campus Wi-Fi and off-campus VPN"),
              bullet("Learning portal and assignment submissions"), bullet("Printing and technical support"),
              Spacer(1, 0.45 * inch), para("For this demo, all service names, web addresses, hours, limits, and procedures are fictional sample values.", "SmallNote"), PageBreak()])

# Page 2
story.extend([para("1. Student account and password", "SectionTitle"),
              para("Your Sample University account provides access to the learning portal, campus Wi-Fi, library resources, and student email. Your username is your eight-digit student ID. Never share your password or one-time verification code.") ,
              para("Sign in and multi-factor authentication", "SubTitle"),
              bullet("Use your student ID and current password on university sign-in pages."),
              bullet("Approve the multi-factor authentication (MFA) prompt only when you initiated the sign-in."),
              bullet("If you receive an unexpected MFA prompt, deny it and contact the Service Desk."),
              para("Reset a forgotten password", "SubTitle"),
              para("Visit <b>accounts.sampleu.example/password-reset</b>, enter your student ID, and complete identity verification using your registered recovery email. Choose a new password that you do not use on other websites. The reset link expires after 30 minutes."),
              callout("After five consecutive incorrect password attempts, sign-in is temporarily locked for 15 minutes. If the lockout continues after that period, contact the Service Desk."),
              para("Account safety", "SubTitle"),
              bullet("The university will not ask you to send a password by email."),
              bullet("Sign out on shared computers and remove saved credentials from public devices."),
              bullet("Report a suspected account compromise to <b>support@sampleu.example</b> as soon as possible."), PageBreak()])

# Page 3
story.extend([para("2. Wi-Fi and off-campus access", "SectionTitle"),
              para("Connect to campus Wi-Fi", "SubTitle"),
              para("On campus, select the wireless network <b>SampleU-Student</b>. Sign in with your eight-digit student ID and university password, then approve the MFA prompt. The network may ask you to sign in again every 30 days."),
              bullet("If the sign-in page does not appear, open a browser and visit <b>http://connect.sampleu.example</b>."),
              bullet("Remove older saved SampleU-Student profiles if your password has changed."),
              bullet("Do not use open guest Wi-Fi for university account access."),
              para("Use the university VPN away from campus", "SubTitle"),
              para("The SampleU VPN is intended for off-campus access to licensed library resources and internal systems. Install the SampleU VPN client from <b>software.sampleu.example/vpn</b>, sign in with your student account, and approve MFA. Disconnect when you finish using the protected resource."),
              callout("The VPN is not required for the public learning portal or ordinary web browsing. VPN access is available to currently enrolled students."),
              para("Connection troubleshooting", "SubTitle"),
              bullet("Check that your device date and time are set automatically."),
              bullet("Restart Wi-Fi, forget the saved network, and reconnect using your current password."),
              bullet("If VPN sign-in fails twice, wait five minutes before trying again. Contact the Service Desk if the issue continues."), PageBreak()])

# Page 4
story.extend([para("3. Learning portal and coursework", "SectionTitle"),
              para("The SampleU Learning Portal is at <b>learn.sampleu.example</b>. Sign in using your student ID and university password. Course pages, announcements, reading materials, and assignment submissions appear in the portal."),
              para("Submit an assignment", "SubTitle"),
              bullet("Open the correct course and assignment before uploading your file."),
              bullet("Accepted file types are PDF, DOCX, XLSX, PPTX, and ZIP. The maximum upload size is 100 MB."),
              bullet("Select Submit, choose the file, and wait for the confirmation screen."),
              bullet("Save the submission receipt shown after upload. A draft or upload-progress screen is not a submission receipt."),
              para("Deadlines and updates", "SubTitle"),
              para("Deadlines are displayed in the time zone configured in your portal profile. The portal receipt shows the recorded submission time. If a course page and a downloaded copy differ, check the latest announcement or ask the course instructor."),
              callout("The Service Desk can help with sign-in, upload errors, and portal access. It cannot change grades, extend deadlines, or decide whether late work is accepted. Contact your instructor about course rules."),
              para("If upload fails", "SubTitle"),
              bullet("Confirm the file is smaller than 100 MB and has an accepted file type."),
              bullet("Try a current browser and a stable internet connection."),
              bullet("Take a screenshot of the error and contact support@sampleu.example before the deadline."), PageBreak()])

# Page 5
story.extend([para("4. Printing and technical support", "SectionTitle"),
              para("Student printing", "SubTitle"),
              para("Students receive a sample monthly allowance of 50 black-and-white pages. Print jobs are released at a campus printer using your student ID card. Unreleased print jobs are deleted after 24 hours. This demo manual does not define color-printing charges."),
              bullet("Check the printer name and page count before sending a job."),
              bullet("If a job is stuck, cancel it in the print queue and resend once."),
              bullet("For an unreadable or jammed printer, note the printer location and contact the Service Desk."),
              para("Contact the Service Desk", "SubTitle"),
              para("Email <b>support@sampleu.example</b> or visit the Student Service Desk in Building A, Room 104. Sample walk-in hours are Monday to Friday, 9:00 a.m. to 5:00 p.m., excluding university holidays. Include your student ID, device type, the service affected, and a brief description of the error. Never include your password."),
              para("Response and urgent issues", "SubTitle"),
              para("The sample target for a first email response is two working days. This is a target, not a guarantee. For a suspected account compromise, include <b>SECURITY</b> in the email subject and call the Service Desk during walk-in hours."),
              callout("This fictional manual does not provide emergency, medical, campus-safety, or real account-recovery guidance. Use your institution's official contacts for real situations."),
              Spacer(1, 0.15 * inch), para("End of sample manual  /  Version 1.0  /  Created for a student QA project", "SmallNote")])

doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=0.78 * inch, leftMargin=0.78 * inch, topMargin=0.76 * inch, bottomMargin=0.78 * inch, title="Sample University Student IT Services Manual", author="Student QA Project")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT.resolve())
