---
title: "Include THM-Medium-rated"
date: 2026-01-06T21:46:30+00:00
draft: false
categories: [""]
tags: []
---


# Include - Penetration Test Walkthrough

This note details the steps taken during a penetration test, focusing on identifying and exploiting vulnerabilities across multiple services to achieve full system compromise and retrieve flags.

## 1. Initial Reconnaissance

The first step involved network scanning to identify open ports and services.

-   **Rustscan:** Used for initial rapid port scanning.
    ![Pasted image 20260106142820.png](/images/Pasted%20image%2020260106142820.png)
-   **Nmap:** Followed up with a more detailed Nmap scan to enumerate services and versions.
    ![Pasted image 20260106143356.png](/images/Pasted%20image%2020260106143356.png)
    ![Pasted image 20260106143411.png](/images/Pasted%20image%2020260106143411.png)

**Key Findings:**
-   Several mail servers were open, but the focus was shifted to web services.
-   Web services were identified on ports `4000` and `50000`.

## 2. Exploiting the Web Application on Port 4000

### 2.1 Initial Access and IDOR Discovery

-   **Login:** Visiting port `4000` revealed a login page. Provided credentials (not specified in the original note, but implied they worked) successfully granted access.
    ![Pasted image 20260106143621.png](/images/Pasted%20image%2020260106143621.png)
    ![Pasted image 20260106143643.png](/images/Pasted%20image%2020260106143643.png)
-   **Insecure Direct Object Reference (IDOR):** Incrementing the user ID in the URL allowed viewing other user profiles without proper authorization. Burp Intruder was used to test for other users, but no higher-privileged accounts were immediately found this way.
    ![Pasted image 20260106144049.png](/images/Pasted%20image%2020260106144049.png)
-   Attempting to log in as 'admin' with various passwords after signing out was unsuccessful.
    ![Pasted image 20260106144212.png](/images/Pasted%20image%2020260106144212.png)

### 2.2 Privilege Escalation via IDOR

-   **Modifying User Information:** The application had a "recommend an activity" functionality.
    ![Pasted image 20260106155642.png](/images/Pasted%20image%2020260106155642.png)
    ![Pasted image 20260106155838.png](/images/Pasted%20image%2020260106155838.png)
-   It was discovered that user information, such as age, could be modified.
    -   Changed age from 25 to 30:
        ![Pasted image 20260106160000.png](/images/Pasted%20image%2020260106160000.png)
        ![Pasted image 20260106160016.png](/images/Pasted%20image%2020260106160016.png)
        ![Pasted image 20260106160051.png](/images/Pasted%20image%2020260106160051.png)
-   **Admin Privilege Escalation:** This led to the attempt to modify the `IsAdmin` field from `false` to `true`.
    ![Pasted image 20260106160313.png](/images/Pasted%20image%2020260106160313.png)
    ![Pasted image 20260106160356.png](/images/Pasted%20image%2020260106160356.png)
-   This modification was successful, granting administrative privileges and revealing two new functionalities: "API" and "Settings".
    ![Pasted image 20260106185831.png](/images/Pasted%20image%2020260106185831.png)

### 2.3 Server-Side Request Forgery (SSRF)

-   **API Section:** The API section revealed a URL to an endpoint `/internal-api` on port `5000`.
    ![Pasted image 20260106192519.png](/images/Pasted%20image%2020260106192519.png)
-   **Settings Section - Update Banner Image URL:** The "Settings" section contained a functionality to update the banner image, which received calls from external domains. This was identified as a potential SSRF vulnerability.
-   **Exploiting SSRF:** The internal endpoint `/getAllAdmins101099991` was supplied to the "Update Banner Image URL" field.
    ![Pasted image 20260106192919.png](/images/Pasted%20image%2020260106192919.png)
-   The server processed the request and returned the data as a Base64 encoded Data URI.
    ![Pasted image 20260106193121.png](/images/Pasted%20image%2020260106193121.png)
-   **Credential Disclosure:** Decoding the Base64 string in Burp Decoder revealed credentials for the `sysmon` instance running on port `50000`.
    ![Pasted image 20260106193547.png](/images/Pasted%20image%2020260106193547.png)

## 3. Accessing and Exploiting Sysmon on Port 50000

### 3.1 Initial Access and Flag Retrieval

-   **Login:** Using the credentials obtained via SSRF, successful login to the `sysmon` instance on port `50000` was achieved.
    ![Pasted image 20260106201421.png](/images/Pasted%20image%2020260106201421.png)
-   A flag was found immediately upon login.

### 3.2 Local File Inclusion (LFI)

-   **Vulnerability Discovery:** Leaving an input field empty on the `sysmon` application resulted in a response that indicated a possible Local File Inclusion (LFI) vulnerability.
    ![Pasted image 20260106195439.png](/images/Pasted%20image%2020260106195439.png)
-   **Exploiting LFI:** Fuzzing confirmed the LFI vulnerability. The payload `....//....//....//....//....//....//....//....//....//etc/passwd` was used to retrieve the contents of `/etc/passwd`.
    ![Pasted image 20260106213513.png](/images/Pasted%20image%2020260106213513.png)
    ![Pasted image 20260106211818.png](/images/Pasted%20image%2020260106211818.png)
-   The user list from `/etc/passwd` was extracted and saved for further brute-forcing attempts.

## 4. SSH Access and Final Flag

-   **SSH Brute-forcing:** The users obtained from `/etc/passwd` were combined with the previously found credentials (and potentially other common passwords) to brute-force SSH access.
    ![Pasted image 20260106211957.png](/images/Pasted%20image%2020260106211957.png)
-   **Successful SSH Login:** Valid credentials were found, allowing successful SSH access to the server.
-   **Final Flag:** The last required flag was located in the `/var/www/html/` directory.
    ![Pasted image 20260106212145.png](/images/Pasted%20image%2020260106212145.png)

This concludes the penetration test, with all flags successfully retrieved.

