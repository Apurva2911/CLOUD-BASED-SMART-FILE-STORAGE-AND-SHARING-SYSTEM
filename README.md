# CLOUD-BASED-SMART-FILE-STORAGE-AND-SHARING-SYSTEM

## Project Overview
SmartDrive is a **secure, serverless file management system** that allows users to upload, store, manage, and share files in the cloud. The system leverages **AWS services** to provide a scalable, reliable, and fully serverless solution with JWT-based authentication and optional CloudFront CDN for faster file access.

---
## Testing the Project/URL
[SmartDrive CloudFront Link]

https://d37vylmpmkwy2d.cloudfront.net/

**Username:** Apurva kadam  
**Password:** Apurva@123  

## Project Goal
- Provide a secure platform for file upload, storage, and management.  
- Implement a serverless architecture to minimize maintenance and maximize scalability.  
- Enable fast, secure access to files with HTTPS/SSL and optional CDN support.  

---

## Tools & Technologies
| Layer        | Tools / Services                                 |
|--------------|--------------------------------------------------|
| Frontend     | HTML, CSS, JavaScript                            |
| Backend      | AWS Lambda, API Gateway                          |
| Storage      | AWS S3                                          |
| Database     | DynamoDB (`SmartDriveFiles` table)              |
| Security     | JWT Authentication, SSL/HTTPS                   |
| Optional     | CloudFront CDN                                  |
| Other        | Base64 encoding for file transfer, CORS configured |

---

## System Features
- **JWT-secured login** for secure access  
- **File Upload** via frontend → Lambda → S3  
- **Metadata Storage**: `file_id`, `filename`, `owner_email`, `upload_date` in DynamoDB  
- **File Operations**: List, Download, Delete, Share (pre-signed URLs)  
- **Serverless, scalable, and secure**

---

## Workflow Overview
- The workflow diagram is included in the project documentation (`docs/Workflow_Diagram.png`).  
- **High-level flow**:  
  1. User logs in (JWT-secured)  
  2. File upload → Frontend encodes to Base64 → Lambda → S3  
  3. Metadata stored in DynamoDB  
  4. Users can list, download, delete, and share files  

---

## Demo Screenshots
- Login Page  
- File Upload / List Page  
- Download / Share / Delete Features  
- Report word file uploaded 

---

## Security & Performance
- JWT Authentication ensures secure access  
- HTTPS/SSL for encrypted data transfer  
- CORS enabled for frontend-backend communication  
- CloudFront CDN (optional) for faster file delivery globally  

---

## Testing the Project

### Demo Account
- **Username:** Apurva kadam  
- **Password:** Apurva@123  

### Steps to Test
1. Open the website and login using the demo credentials.  
2. Upload a file and confirm it appears in the file list.  
3. Download, delete, and share files to test functionality.  
4. (Optional) Check metadata in DynamoDB (`file_id`, `filename`, `owner_email`, `upload_date`).  

> Note: This is a demo account. Do not use personal files.

---


