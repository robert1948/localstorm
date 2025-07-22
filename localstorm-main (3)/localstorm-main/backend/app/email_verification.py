"""
Email verification code functionality for authentication
"""
import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from .database import Base
from .email_service import EmailService
from typing import Optional

class VerificationCode(Base):
    """Email verification codes for authentication"""
    __tablename__ = "verification_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    code = Column(String(6), nullable=False)
    purpose = Column(String, nullable=False)  # "login", "registration", "password_reset"
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
    is_used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

class EmailVerificationService:
    def __init__(self):
        self.email_service = EmailService()
        
    def generate_code(self) -> str:
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    async def send_login_code(
        self, 
        db: Session, 
        email: str, 
        user_agent: str = None, 
        ip_address: str = None
    ) -> bool:
        """Send login verification code via email"""
        
        # Generate new code
        code = self.generate_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)  # 10 minute expiry
        
        # Invalidate any existing unused codes for this email and purpose
        db.query(VerificationCode).filter(
            VerificationCode.email == email,
            VerificationCode.purpose == "login",
            VerificationCode.is_used == False
        ).update({"is_used": True, "used_at": datetime.utcnow()})
        
        # Create new verification code
        verification = VerificationCode(
            email=email,
            code=code,
            purpose="login",
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address
        )
        db.add(verification)
        db.commit()
        db.refresh(verification)
        
        # Send email
        success = await self._send_verification_email(email, code, "login")
        return success
    
    async def verify_login_code(
        self, 
        db: Session, 
        email: str, 
        code: str
    ) -> tuple[bool, str]:
        """Verify login code and return (success, message)"""
        
        # Find the most recent unused code for this email
        verification = db.query(VerificationCode).filter(
            VerificationCode.email == email,
            VerificationCode.purpose == "login",
            VerificationCode.is_used == False,
            VerificationCode.expires_at > datetime.utcnow()
        ).order_by(VerificationCode.created_at.desc()).first()
        
        if not verification:
            return False, "No valid verification code found. Please request a new one."
        
        # Increment attempts
        verification.attempts += 1
        db.commit()
        
        # Check if too many attempts
        if verification.attempts > 3:
            verification.is_used = True
            verification.used_at = datetime.utcnow()
            db.commit()
            return False, "Too many failed attempts. Please request a new verification code."
        
        # Check if code matches
        if verification.code != code:
            db.commit()
            return False, f"Invalid verification code. {4 - verification.attempts} attempts remaining."
        
        # Mark as used
        verification.is_used = True
        verification.used_at = datetime.utcnow()
        db.commit()
        
        return True, "Verification successful"
    
    async def _send_verification_email(self, email: str, code: str, purpose: str) -> bool:
        """Send verification code email"""
        
        if purpose == "login":
            subject = "CapeControl Login Verification Code"
            html_content = self._get_login_email_template(code)
        else:
            subject = "CapeControl Verification Code"
            html_content = self._get_generic_email_template(code, purpose)
        
        return await self.email_service.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content
        )
    
    def _get_login_email_template(self, code: str) -> str:
        """Get HTML template for login verification email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login Verification - CapeControl</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4F46E5; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .code-box {{ 
                    background: white; 
                    border: 3px solid #4F46E5; 
                    padding: 20px; 
                    text-align: center; 
                    margin: 20px 0; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .code {{ 
                    font-size: 32px; 
                    font-weight: bold; 
                    color: #4F46E5; 
                    letter-spacing: 8px;
                    font-family: 'Courier New', monospace;
                }}
                .warning {{ 
                    background: #FEF3C7; 
                    border-left: 4px solid #F59E0B; 
                    padding: 15px; 
                    margin: 20px 0; 
                    border-radius: 5px;
                }}
                .footer {{ 
                    text-align: center; 
                    padding: 20px; 
                    color: #666; 
                    font-size: 0.9em; 
                }}
                .btn {{
                    display: inline-block;
                    background: #4F46E5;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Login Verification</h1>
                    <p style="margin: 0; font-size: 18px;">Secure access to your CapeControl account</p>
                </div>
                
                <div class="content">
                    <h2>Hi there!</h2>
                    <p>Someone is trying to log in to your CapeControl account. To complete the login process, please use the verification code below:</p>
                    
                    <div class="code-box">
                        <div class="code">{code}</div>
                        <p style="margin: 10px 0 0 0; color: #666;">Enter this code in your login form</p>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul style="margin: 10px 0 0 0;">
                            <li>This code expires in <strong>10 minutes</strong></li>
                            <li>Never share this code with anyone</li>
                            <li>CapeControl will never ask for this code via phone or email</li>
                        </ul>
                    </div>
                    
                    <p>If you didn't request this login, please ignore this email and consider changing your password for security.</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://cape-control.com/login" class="btn">Complete Login →</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This is an automated security email from CapeControl.<br>
                    Need help? Contact us at <a href="mailto:support@capecontrol.com">support@capecontrol.com</a></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_generic_email_template(self, code: str, purpose: str) -> str:
        """Get HTML template for generic verification email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Verification Code - CapeControl</title>
        </head>
        <body>
            <h2>Verification Code</h2>
            <p>Your {purpose} verification code is: <strong>{code}</strong></p>
            <p>This code expires in 10 minutes.</p>
        </body>
        </html>
        """

# Global instance
email_verification_service = EmailVerificationService()
