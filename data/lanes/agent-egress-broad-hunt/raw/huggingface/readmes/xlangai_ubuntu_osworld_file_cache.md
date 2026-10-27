---
license: apache-2.0
---
# OSWorld File Cache

This repository serves as a file cache for the [OSWorld](https://github.com/xlang-ai/OSWorld) project, providing reliable and fast access to evaluation files that were previously hosted on Google Drive.

## Overview

OSWorld is a scalable, real computer environment for multimodal agents, supporting task setup, execution-based evaluation, and interactive learning across various operating systems and applications. This cache repository ensures that all evaluation files are consistently accessible for research and development purposes.

## Repository Structure

The files are organized by application categories, mirroring the structure of the original OSWorld evaluation examples:

```
├── chrome/                 # Chrome browser evaluation files
├── firefox/               # Firefox browser evaluation files  
├── gimp/                  # GIMP image editor evaluation files
├── libreoffice_calc/      # LibreOffice Calc spreadsheet files
├── libreoffice_impress/   # LibreOffice Impress presentation files
├── libreoffice_writer/    # LibreOffice Writer document files
├── multi_apps/            # Multi-application evaluation files
├── thunderbird/           # Thunderbird email client files
├── vscode/                # Visual Studio Code editor files
└── ...                    # Other application categories
```

Each application folder contains subfolders named after specific evaluation scenarios, with the actual files (images, documents, datasets, etc.) used in those evaluations.

## Usage

### Direct File Access

Files can be accessed directly via their URLs in the format:
```
https://huggingface.co/datasets/xlangai/ubuntu_osworld_file_cache/resolve/main/{app_name}/{scenario_id}/{filename}
```

### Integration with OSWorld

This cache is automatically integrated with OSWorld evaluation scripts. The original Google Drive URLs in the evaluation JSON files have been migrated to point to this HuggingFace cache, ensuring:

- **Reliability**: No more broken or inaccessible Google Drive links
- **Performance**: Faster download speeds and better availability
- **Consistency**: Stable file versions for reproducible research

### Programmatic Access

You can use the HuggingFace Hub library to access files programmatically:

from huggingface_hub import hf_hub_download

# Download a specific file
```
file_path = hf_hub_download(
    repo_id="xlangai/ubuntu_osworld_file_cache",
    filename="chrome/scenario_123/test_image.png",
    repo_type="dataset"
)
```

## File Types

This cache contains various types of files used in OSWorld evaluations:

- **Images**: Screenshots, reference images, icons (PNG, JPG, GIF, etc.)
- **Documents**: Text files, PDFs, spreadsheets, presentations
- **Media**: Audio and video files for multimedia evaluations
- **Data**: CSV files, JSON configurations, datasets
- **Archives**: ZIP files containing multiple evaluation assets

## Migration Information

This repository was created by migrating files from Google Drive to ensure better accessibility and reliability. The migration process:

1. **Preserved file integrity**: All files maintain their original content and format
2. **Maintained naming**: Original filenames are preserved where possible
3. **Updated references**: All OSWorld JSON configuration files have been updated to use the new URLs
4. **Added redundancy**: Files are now hosted on HuggingFace's robust infrastructure

## Contributing

If you encounter any issues with file accessibility or notice missing files, please:

1. Check the original OSWorld repository for the latest evaluation configurations
2. Open an issue in the [OSWorld GitHub repository](https://github.com/xlang-ai/OSWorld)
3. Provide specific details about the missing or problematic files

## License

The files in this repository are subject to the same licensing terms as the original OSWorld project. Please refer to the [OSWorld repository](https://github.com/xlang-ai/OSWorld) for detailed licensing information.

## Related Projects

- **[OSWorld](https://github.com/xlang-ai/OSWorld)**: The main OSWorld project repository
- **[OSWorld Paper](https://arxiv.org/abs/2404.07972)**: Research paper describing the OSWorld framework
- **[XLang Lab](https://github.com/xlang-ai)**: Organization behind OSWorld and related research

## Technical Details

- **Storage**: Files are stored using HuggingFace's Git LFS (Large File Storage) system
- **Access**: Public read access, no authentication required
- **Bandwidth**: Leverages HuggingFace's global CDN for fast access worldwide
- **Versioning**: Files are version-controlled using Git, ensuring reproducibility

## Support

For technical support or questions about this file cache:

- **OSWorld Issues**: [GitHub Issues](https://github.com/xlang-ai/OSWorld/issues)
- **HuggingFace Support**: [HuggingFace Community](https://huggingface.co/discussions)
- **Research Inquiries**: Contact the XLang Lab team

---

*This cache repository is maintained as part of the OSWorld project to support reproducible research in multimodal AI agents and computer automation.*