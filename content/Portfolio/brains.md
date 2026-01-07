---
title: "Brains"
date: 2026-01-04T23:15:04+00:00
draft: false
toc: true
categories: [""]
tags: []
---


Ping the target to confirm it is up and running... 

{{< figure src="/images/Pasted-image-20251229105227.png"->}}

Recon-

{{<-figure-src="/images/Pasted-image-20251229105809.png"->}}

4-open-ports.-22,-80,-43209,-50000.-

Scanning-

Nmap-to-actively-scan-the-target,-ssh-is-open-on-22,-a-weberver-running-on-port-80-and-50000-hosting-tomcat.-

although-one-port-from-rustscan-43209-doesnt-show-on-the-nmap-scan,-we-will-scan-specifcally-to-make-sure-we-missed-nothing..-

{{<-figure-src="/images/Pasted-image-20251229110207.png"->}}

we-have-it-here-and-hosts-java-rmi-
{{<-figure-src="/images/Pasted-image-20251229111318.png"->}}


Enumeration->--

Visit-the-website-running-on-port-80..

{{<-figure-src="/images/Pasted-image-20251229110051.png"->}}




Checking-the-website-on-port-50000,-we-have-a-login-page-using-the-software-teamcityand-requires-a-login-credentials.-

{{<-figure-src="/images/Pasted-image-20251229155408.png" >}}

attempted using default credentials but none worked.. 

Researched if the teamcity has any known exploit and lo and behold, there is a vulnerability affecting the particular version even an unauthenticated remote code execution.. 
  
CVE-2024-27198 is an authentication bypass vulnerability in the web component of TeamCity that arises from an alternative path issue ([CWE-288](https://cwe.mitre.org/data/definitions/288.html)) and has a CVSS base score of 9.8 (Critical).


The exploit is available in metasploit as well hence what i will be using . 

{{< figure src="/images/Pasted-image-20251229160306.png"->}}

Navigating-to-the-user-directory-we-have-the-flag...-

{{<-figure-src="/images/Pasted-image-20251229162905.png"->}}

And-that's-the-of-the-red-exploit-the-server-section-and-we-are-moving-to-the-blue-section..-


{{<-figure-src="/images/Pasted-image-20251229163710.png"->}}

{{<-figure-src="/images/Pasted-image-20251229165038.png"->}}


Logged-into-the-Splunk-instance.

{{<-figure-src="/images/Pasted-image-20251229164520.png" >}}

