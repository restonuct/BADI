"""
System Control Module

Provides file system operations, organization, and management capabilities.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

from badi.modules.base import Module, ModuleCapability, ModuleParameter, register_module

logger = logging.getLogger(__name__)


class SystemControlModule(Module):
    """
    System control and file management module
    
    Provides capabilities for:
    - Scanning directories
    - Moving/organizing files
    - Cleanup operations
    - File information
    """
    
    name = "system_control"
    description = "File system operations and management"
    version = "1.0.0"
    requires_confirmation = True  # File operations require confirmation
    is_read_only = False
    
    capabilities = [
        ModuleCapability(
            name="scan_directory",
            description="Scan a directory and list files with details",
            parameters=[
                ModuleParameter(
                    name="path",
                    type="string",
                    description="Directory path to scan",
                    required=True
                ),
                ModuleParameter(
                    name="recursive",
                    type="bool",
                    description="Scan subdirectories recursively",
                    required=False,
                    default=False
                ),
                ModuleParameter(
                    name="file_types",
                    type="list",
                    description="Filter by file extensions (e.g., ['.pdf', '.txt'])",
                    required=False,
                    default=None
                )
            ],
            examples=[
                "scan_directory: path='~/Downloads', recursive=False",
                "scan_directory: path='~/Documents', recursive=True, file_types=['.pdf', '.docx']"
            ]
        ),
        ModuleCapability(
            name="move_old_files",
            description="Move files older than specified days to archive folder",
            parameters=[
                ModuleParameter(
                    name="source_path",
                    type="string",
                    description="Source directory path",
                    required=True
                ),
                ModuleParameter(
                    name="days",
                    type="int",
                    description="Files older than this many days",
                    required=True
                ),
                ModuleParameter(
                    name="archive_path",
                    type="string",
                    description="Archive destination (default: source_path/archive)",
                    required=False,
                    default=None
                )
            ],
            examples=[
                "move_old_files: source_path='~/Downloads', days=30"
            ]
        ),
        ModuleCapability(
            name="organize_by_type",
            description="Organize files into folders by file type",
            parameters=[
                ModuleParameter(
                    name="source_path",
                    type="string",
                    description="Directory to organize",
                    required=True
                ),
                ModuleParameter(
                    name="create_folders",
                    type="bool",
                    description="Create type-based folders (Documents, Images, etc.)",
                    required=False,
                    default=True
                )
            ],
            examples=[
                "organize_by_type: source_path='~/Downloads'"
            ]
        ),
        ModuleCapability(
            name="get_file_info",
            description="Get detailed information about a file",
            parameters=[
                ModuleParameter(
                    name="file_path",
                    type="string",
                    description="Path to file",
                    required=True
                )
            ]
        )
    ]
    
    def __init__(self):
        super().__init__()
        
        # File type categories
        self.type_categories = {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
            "Spreadsheets": [".xlsx", ".xls", ".csv"],
            "Presentations": [".pptx", ".ppt", ".key"]
        }
    
    async def run(self, capability: str, **kwargs) -> Dict[str, Any]:
        """Execute a capability"""
        # Validate parameters
        valid, error = self.validate_parameters(capability, kwargs)
        if not valid:
            return {"success": False, "error": error}
        
        try:
            if capability == "scan_directory":
                return await self._scan_directory(**kwargs)
            elif capability == "move_old_files":
                return await self._move_old_files(**kwargs)
            elif capability == "organize_by_type":
                return await self._organize_by_type(**kwargs)
            elif capability == "get_file_info":
                return await self._get_file_info(**kwargs)
            else:
                return {"success": False, "error": f"Unknown capability: {capability}"}
        except Exception as e:
            self.logger.error(f"Error executing {capability}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _scan_directory(
        self,
        path: str,
        recursive: bool = False,
        file_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Scan directory and return file list"""
        directory = Path(path).expanduser()
        
        if not directory.exists():
            return {"success": False, "error": f"Directory not found: {path}"}
        
        if not directory.is_dir():
            return {"success": False, "error": f"Not a directory: {path}"}
        
        files = []
        pattern = "**/*" if recursive else "*"
        
        for item in directory.glob(pattern):
            if item.is_file():
                # Filter by file type if specified
                if file_types and item.suffix.lower() not in [ft.lower() for ft in file_types]:
                    continue
                
                stat = item.stat()
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "size": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "extension": item.suffix
                })
        
        # Sort by modified date (newest first)
        files.sort(key=lambda x: x["modified"], reverse=True)
        
        return {
            "success": True,
            "result": {
                "directory": str(directory),
                "file_count": len(files),
                "total_size_mb": round(sum(f["size"] for f in files) / (1024 * 1024), 2),
                "files": files
            }
        }
    
    async def _move_old_files(
        self,
        source_path: str,
        days: int,
        archive_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Move old files to archive"""
        source = Path(source_path).expanduser()
        
        if not source.exists() or not source.is_dir():
            return {"success": False, "error": f"Invalid source directory: {source_path}"}
        
        # Set archive path
        if archive_path:
            archive = Path(archive_path).expanduser()
        else:
            archive = source / "archive"
        
        # Create archive directory
        archive.mkdir(parents=True, exist_ok=True)
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=days)
        
        moved_files = []
        errors = []
        
        for item in source.iterdir():
            if item.is_file():
                stat = item.stat()
                modified_date = datetime.fromtimestamp(stat.st_mtime)
                
                if modified_date < cutoff_date:
                    try:
                        dest = archive / item.name
                        # Handle name conflicts
                        counter = 1
                        while dest.exists():
                            name = f"{item.stem}_{counter}{item.suffix}"
                            dest = archive / name
                            counter += 1
                        
                        shutil.move(str(item), str(dest))
                        moved_files.append({
                            "name": item.name,
                            "original_path": str(item),
                            "new_path": str(dest),
                            "age_days": (datetime.now() - modified_date).days
                        })
                    except Exception as e:
                        errors.append({"file": item.name, "error": str(e)})
        
        return {
            "success": True,
            "result": {
                "moved_count": len(moved_files),
                "archive_path": str(archive),
                "moved_files": moved_files,
                "errors": errors
            }
        }
    
    async def _organize_by_type(
        self,
        source_path: str,
        create_folders: bool = True
    ) -> Dict[str, Any]:
        """Organize files by type into folders"""
        source = Path(source_path).expanduser()
        
        if not source.exists() or not source.is_dir():
            return {"success": False, "error": f"Invalid directory: {source_path}"}
        
        organized = {}
        errors = []
        
        for item in source.iterdir():
            if item.is_file():
                # Determine category
                category = "Other"
                for cat_name, extensions in self.type_categories.items():
                    if item.suffix.lower() in [ext.lower() for ext in extensions]:
                        category = cat_name
                        break
                
                if create_folders:
                    # Create category folder
                    dest_folder = source / category
                    dest_folder.mkdir(exist_ok=True)
                    dest = dest_folder / item.name
                    
                    try:
                        # Handle name conflicts
                        counter = 1
                        while dest.exists():
                            name = f"{item.stem}_{counter}{item.suffix}"
                            dest = dest_folder / name
                            counter += 1
                        
                        shutil.move(str(item), str(dest))
                        
                        if category not in organized:
                            organized[category] = []
                        organized[category].append(item.name)
                    except Exception as e:
                        errors.append({"file": item.name, "error": str(e)})
        
        return {
            "success": True,
            "result": {
                "organized_count": sum(len(files) for files in organized.values()),
                "categories": organized,
                "errors": errors
            }
        }
    
    async def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get file information"""
        file = Path(file_path).expanduser()
        
        if not file.exists():
            return {"success": False, "error": f"File not found: {file_path}"}
        
        if not file.is_file():
            return {"success": False, "error": f"Not a file: {file_path}"}
        
        stat = file.stat()
        
        return {
            "success": True,
            "result": {
                "name": file.name,
                "path": str(file),
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "extension": file.suffix,
                "is_hidden": file.name.startswith(".")
            }
        }


# Auto-register module on import
register_module(SystemControlModule())
