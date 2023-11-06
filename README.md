<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![MIT License][license-shield]][license-url]

<h3 align="center">AssetPoint Weekly BI</h3>

  <p align="center">
    A module for fetching data from the salesforce api to populate the Power BI dashboard for the AssetPoint Support weekly meeting.
    <br />
    <a href="https://github.com/spierce5/assetpoint-weekly-bi/issues">Report Bug</a>
    ·
    <a href="https://github.com/spierce5/assetpoint-weekly-bi/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#setup">Setup</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

A module for fetching data from the salesforce api to populate the Power BI dashboard for the AssetPoint Support weekly meeting.

This was originally developed for generating a weekly PowerPoint, but has been modified to be used as a service to fetch data for Power BI.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

Please ensure you have the following requirements installed before going further. Failure to do so will likely prevent you from properly installing the module.

- Python 3.11.5 - Download and install from <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>
- Git - Download and install from <a href="https://github.com/git-guides/install-git">https://github.com/git-guides/install-git</a>
- Microsoft Visual C++ 14.0 - Download and install from <a href="https://visualstudio.microsoft.com/visual-cpp-build-tools/">https://visualstudio.microsoft.com/visual-cpp-build-tools/</a>
  - In the Visual Studio installer, you only need to select "Desktop development with C++"

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/spierce5/assetpoint-weekly-bi.git
   ```
2. Change directory to the project folder
   ```sh
   cd assetpoint-weekly-bi
   ```
3. Install PIP packages
   ```sh
   pip install -r requirements.txt
   ```

### Setup

Several further setup steps are required before use. Two additional files will need to be created:

- .env
- app_data.json

You can copy from .env.example and app_data.json.example respectively.

#### .env

In order to connect to Salesforce, you will need to update the environment variables in .env as such:

<table>
  <thead style="border: 1px solid #333;">
    <tr>
      <th colspan="2">/.env</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #333;">Key</td>
      <td style="border: 1px solid #333;">Description</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">SF_INSTANCE</td>
      <td style="border: 1px solid #333;">Your organization's Salesforce domain</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">SF_USERNAME</td>
      <td style="border: 1px solid #333;">Your Salesforce username found in Setup</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">SF_PASSWORD</td>
      <td style="border: 1px solid #333;">Your Salesforce password</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">SF_TOKEN</td>
      <td style="border: 1px solid #333;">Your Salesforce security token</td>
    </tr>
  </tbody>
</table>

You will need to set a password for your Salesforce account on the Setup page. Once your password is set, you should receive an email with your security token, otherwise, you can generate a new security token manually. Read more at <a href="https://help.salesforce.com/s/articleView?id=sf.user_security_token.htm&type=5">https://help.salesforce.com/s/articleView?id=sf.user_security_token.htm&type=5</a>

#### app_data.json

The content of app_data.json must be valid json and must contain a key named "team_members". Within team_members, you will need to add the following information:

<table>
  <thead style="border: 1px solid #333;">
    <tr>
      <th colspan="2">/app_data.json - team_members</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #333;">Key</td>
      <td style="border: 1px solid #333;">Description</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">name</td>
      <td style="border: 1px solid #333;">Full name as used in Salesforce</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">preferred_name</td>
      <td style="border: 1px solid #333;">Preferred first name e.g. Sam rather than Samuel</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">birthday</td>
      <td style="border: 1px solid #333;">Birthday in yyyy-mm-dd format (year will not be used, but must be a valid year)</td>
    </tr>
    <tr>
      <td style="border: 1px solid #333;">active</td>
      <td style="border: 1px solid #333;">True if a current member of the team, otherwise, False</td>
    </tr>
  </tbody>
</table>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Sam Pierce - sam.pierce@aptean.com

Project Link: [https://github.com/spierce5/assetpoint-weekly-bi](https://github.com/spierce5/assetpoint-weekly-bi)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/spierce5/assetpoint-weekly-bi.svg?style=for-the-badge
[license-url]: https://github.com/spierce5/assetpoint-weekly-bi/blob/main/LICENSE
