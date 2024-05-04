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
<!-- [![Forks][forks-shield]][forks-url] -->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Input Log Server</h3>

  <p align="center">
    This repository contains server code for running the linguistic analysis for the InputLog service.
    <br />
    <br />
    <a href="https://github.com/emanjavacas/inputLog/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

[![project-screenshot]]()


<!-- Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `emanjavacas`, `inputLog`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description` -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python]][Python-url]
* [![Rust][Rust]][Rust-url]
* [![FastAPI][FastAPI]][FastAPI-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

It is recommended to clone or download the repo to your machine (there's no package release, and no necessary package installs).

### Prerequisites

We are using `poetry` and `venv` to take care of dependencies and make sure the development environment is reproducible. We also use `python3.8`, so make sure this version is available on your machine (you can use `pyenv` to manage Python versions).

### Installation

1. Install rust
   1. `curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh`
2. Install hyphenation server
   1. `cd ./hyphenate`
   2. `cargo build`
   3. `cd ..`
3. Prepare environment
   1. Make sure you are running `python3.8`
   2. Navigate to the root of the repository (`inputLog`)
   3. (Recommended), create a `venv`
      1. `python -m venv venv`
      2. `source venv/bin/activate`
   4. `pip install pip --upgrade`
   5. `pip install poetry`
4. Install dependencies
   1. `poetry install`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

The repository fires up a `uvicorn` server to run the linguistic processing.
Syllabification is done with `rust` in a separate process. The main server interacts with the syllabification process over RPC.
All configurations (ports, and more) are specified on the `.env` file.

To run the syllabification server, you need to run:

`cargo run --manifest-path hyphenate/Cargo.toml`

To run the main server, you need to run (on a different shell)

`python main.py`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

No more features are planned as of now.

See the [open issues](https://github.com/emanjavacas/inputLog/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>
 -->

<!-- CONTACT -->
## Contact

See the contributors in this repo.

Project Link: [https://github.com/emanjavacas/inputLog](https://github.com/emanjavacas/inputLog)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/emanjavacas/inputLog.svg?style=for-the-badge
[contributors-url]: https://github.com/emanjavacas/inputLog/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/emanjavacas/inputLog.svg?style=for-the-badge
[forks-url]: https://github.com/emanjavacas/inputLog/network/members
[stars-shield]: https://img.shields.io/github/stars/emanjavacas/inputLog.svg?style=for-the-badge
[stars-url]: https://github.com/emanjavacas/inputLog/stargazers
[issues-shield]: https://img.shields.io/github/issues/emanjavacas/inputLog.svg?style=for-the-badge
[issues-url]: https://github.com/emanjavacas/inputLog/issues
[license-shield]: https://img.shields.io/github/license/emanjavacas/inputLog.svg?style=for-the-badge
[license-url]: https://github.com/emanjavacas/inputLog/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[project-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[PyTorch-url]: https://pytorch.org/
[PyTorch]: https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white
[scikit-learn-url]: https://scikit-learn.org/
[scikit-learn]: https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white
[NumPy-url]: https://numpy.org/
[NumPy]: https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white
[pandas]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[pandas-url]: https://pandas.pydata.org/
[TensorFlow]: https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white
[TensorFlow-url]: https://www.tensorflow.org/
[huggingface]: https://huggingface.co/front/assets/huggingface_logo-noborder.svg
[huggingface-url]: https://huggingface.co
[Rust]: https://img.shields.io/badge/rust-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white
[Rust-url]: https://www.rust-lang.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/