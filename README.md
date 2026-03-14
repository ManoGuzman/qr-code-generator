<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <a href="https://github.com/ManoGuzman/qr-code-generator">
    <img src="https://img.icons8.com/?size=100&id=XdgEzmYg0J8k&format=png&color=000000" alt="QR Logo" width="80" height="80">
  </a>

<h3 align="center">QR Code Generator</h3>

  <p align="center">
    A Python CLI tool that batch-generates QR code PNG images from URLs. Supports single URLs, text files with multiple URLs, and entire directories of URL files — with optional recursive processing.
    <br />
    <a href="https://github.com/ManoGuzman/qr-code-generator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ManoGuzman/qr-code-generator/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ManoGuzman/qr-code-generator/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

`qr-code-generator` is a lightweight Python CLI tool for batch-generating QR code images from URLs. It was originally built to generate personalized QR codes for wedding guests, each encoding a unique RSVP page URL — but it works for any bulk QR code generation need.

Key features:
- Generate a QR code from a single URL directly on the command line
- Process a `.txt` file with one URL per line (supports `#` comment lines)
- Process an entire directory of `.txt` files, with optional recursive traversal
- Auto-sized QR codes with 30% error correction (H-level) saved as PNG files
- Output filenames are automatically derived from the sanitized URL

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![qrcode][qrcode-badge]][qrcode-url]
* [![Pillow][Pillow-badge]][Pillow-url]
* [![Hatch][Hatch-badge]][Hatch-url]
* [![Ruff][Ruff-badge]][Ruff-url]
* [![pytest][pytest-badge]][pytest-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

- Python 3.10 or higher
- `pip` (comes with Python)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ManoGuzman/qr-code-generator.git
   ```
2. Navigate into the project directory
   ```sh
   cd qr-code-generator
   ```
3. Install the package (add `[dev]` to also install test and lint tools)
   ```sh
   pip install ".[dev]"
   ```

This installs the `generate-qr` command globally in your environment.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

All generated QR code PNGs are saved to the `./img/` directory. Output filenames are derived from the sanitized URL (e.g., `https://example.com/path` becomes `example.com_path.png`).

**Generate a QR code from a single URL:**
```sh
generate-qr -f https://example.com
```

**Generate QR codes from a `.txt` file (one URL per line):**
```sh
generate-qr -f links/urls.txt
```

Lines beginning with `#` are treated as comments and skipped. Empty lines are also ignored.

**Generate QR codes from all `.txt` files in a directory:**
```sh
generate-qr -d ./links
```

**Recursively process all `.txt` files in nested subdirectories:**
```sh
generate-qr -d ./links --recursive
```

**Run the test suite:**
```sh
pytest
```

**Run the linter:**
```sh
ruff check src/qr_code_generator/
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Support custom output directory via CLI flag
- [ ] Allow configuring QR code colors (foreground/background)
- [ ] Add support for CSV input files
- [ ] Embed a logo/image into the center of generated QR codes

See the [open issues](https://github.com/ManoGuzman/qr-code-generator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
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

### Top contributors:

<a href="https://github.com/ManoGuzman/qr-code-generator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ManoGuzman/qr-code-generator" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Manuel Guzmán - manuguzman8@gmail.com

Project Link: [https://github.com/ManoGuzman/qr-code-generator](https://github.com/ManoGuzman/qr-code-generator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [qrcode — Python QR Code library](https://github.com/lincolnloop/python-qrcode)
* [Pillow — Python Imaging Library](https://python-pillow.org/)
* [Hatchling — Modern Python build backend](https://hatch.pypa.io/)
* [Ruff — Fast Python linter](https://docs.astral.sh/ruff/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ManoGuzman/qr-code-generator.svg?style=for-the-badge
[contributors-url]: https://github.com/ManoGuzman/qr-code-generator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ManoGuzman/qr-code-generator.svg?style=for-the-badge
[forks-url]: https://github.com/ManoGuzman/qr-code-generator/network/members
[stars-shield]: https://img.shields.io/github/stars/ManoGuzman/qr-code-generator.svg?style=for-the-badge
[stars-url]: https://github.com/ManoGuzman/qr-code-generator/stargazers
[issues-shield]: https://img.shields.io/github/issues/ManoGuzman/qr-code-generator.svg?style=for-the-badge
[issues-url]: https://github.com/ManoGuzman/qr-code-generator/issues
[license-shield]: https://img.shields.io/github/license/ManoGuzman/qr-code-generator.svg?style=for-the-badge
[license-url]: https://github.com/ManoGuzman/qr-code-generator/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/manuel-guzmán-b87b841bb/
<!-- Shields.io badges. You can find a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[qrcode-badge]: https://img.shields.io/badge/qrcode-000000?style=for-the-badge&logo=qrcode&logoColor=white
[qrcode-url]: https://github.com/lincolnloop/python-qrcode
[Pillow-badge]: https://img.shields.io/badge/Pillow-306998?style=for-the-badge&logo=python&logoColor=white
[Pillow-url]: https://python-pillow.org/
[Hatch-badge]: https://img.shields.io/badge/Hatch-009688?style=for-the-badge&logo=python&logoColor=white
[Hatch-url]: https://hatch.pypa.io/
[Ruff-badge]: https://img.shields.io/badge/Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black
[Ruff-url]: https://docs.astral.sh/ruff/
[pytest-badge]: https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white
[pytest-url]: https://docs.pytest.org/
