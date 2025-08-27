#!/usr/bin/env python3
"""Generate Notecard API functions from notecard-schema."""

import requests
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse


class NotecardAPIGenerator:
    """Generate Python API functions from Notecard JSON schema."""

    reserved_keywords = {"in", "out", "from", "import", "class", "def", "if", "else", "for", "while", "try", "except", "with", "as", "is", "not", "and", "or", "async", "await"}

    def __init__(self, schema_url: str = "https://raw.githubusercontent.com/blues/notecard-schema/refs/heads/master/notecard.api.json", notecard_dir: str = "notecard"):
        self.schema_url = schema_url
        self.base_url = "/".join(schema_url.split("/")[:-1]) + "/"
        self.apis = {}
        self.notecard_dir = Path(notecard_dir)

    def fetch_schema(self, url: str, max_retries: int = 3, delay: float = 1.0) -> Dict[str, Any]:
        """Fetch JSON schema from URL with retry logic."""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Error fetching {url} (attempt {attempt + 1}/{max_retries}): {e}")
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                    return {}

    def parse_main_schema(self) -> List[str]:
        """Parse main schema and extract API references."""
        schema = self.fetch_schema(self.schema_url)
        if not schema:
            return []

        refs = []
        if "oneOf" in schema:
            for ref_obj in schema["oneOf"]:
                if "$ref" in ref_obj:
                    refs.append(ref_obj["$ref"])

        return refs

    def parse_api_schema(self, ref_url: str) -> Optional[Dict[str, Any]]:
        """Parse individual API schema and extract information."""
        # Handle both relative and absolute URLs
        if ref_url.startswith("https://"):
            full_url = ref_url
        else:
            full_url = self.base_url + ref_url
        schema = self.fetch_schema(full_url)
        if not schema:
            return None

        # Extract API name from filename
        if "/" in ref_url:
            api_name = ref_url.split("/")[-1].replace(".req.notecard.api.json", "")
        else:
            api_name = ref_url.replace(".req.notecard.api.json", "")

        # Parse properties
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        title = schema.get("title", "")
        description = schema.get("description", "")

        return {
            "name": api_name,
            "title": title,
            "description": description,
            "properties": properties,
            "required": required,
            "schema": schema
        }

    def to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case or dot.separated string to camelCase."""
        # Split on both underscores and dots
        components = snake_str.replace('.', '_').split('_')
        # Keep first component lowercase, capitalize the rest
        return components[0] + ''.join(word.capitalize() for word in components[1:])

    def get_python_type_hint(self, prop: Dict[str, Any]) -> str:
        """Convert JSON schema type to Python type hint."""
        json_type = prop.get("type", "string")

        # Handle case where type is a list of types
        if isinstance(json_type, list):
            # Use the first non-null type
            for t in json_type:
                if t != "null":
                    json_type = t
                    break
            else:
                json_type = "string"

        type_mapping = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict"
        }

        return type_mapping.get(json_type, "str")

    def clean_docstring_text(self, text: str) -> str:
        """Clean up docstring text by removing formatting and compacting markdown."""
        if not text:
            return text

        # Remove newline characters and replace with spaces
        text = text.replace('\n', ' ').replace('\r', ' ')

        # Convert markdown links [text](url) -> text
        import re
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

        # Remove markdown emphasis formatting (* and _)
        # Handle both single and double emphasis markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold** -> bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic* -> italic
        text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__ -> bold
        text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_ -> italic

        # Collapse multiple spaces into single spaces
        text = re.sub(r'\s+', ' ', text)

        # Strip leading/trailing whitespace
        return text.strip()

    def convert_to_imperative_mood(self, text: str) -> str:
        """Convert docstring text to imperative mood using built-in replacements (Pydocstyle D402)."""
        if not text:
            return text

        # Built-in replacements for converting docstrings to imperative mood
        replacements = {
            "Returns": "Return",
            "Configures": "Configure",
            "Performs": "Perform",
            "Used": "Use",
            "Uses": "Use",
            "Sets": "Set",
            "Gets": "Get",
            "Retrieves": "Retrieve",
            "Displays": "Display",
            "Adds": "Add",
            "Enables": "Enable",
            "Provides": "Provide",
            "Deletes": "Delete",
            "Updates": "Update",
            "Calculates": "Calculate",
            "Specifies": "Specify",
            "Determines": "Determine",
            "The": "Use",
            "This": "Use"
        }

        # Apply replacements - only replace at the start of sentences
        for non_imperative, imperative in replacements.items():
            # Replace at the beginning of the text
            if text.startswith(non_imperative + " "):
                text = imperative + text[len(non_imperative):]
                break
            # Also handle cases where the non-imperative word starts the text
            elif text.startswith(non_imperative):
                # Make sure we're not replacing part of a larger word
                if len(text) == len(non_imperative) or not text[len(non_imperative)].isalpha():
                    text = imperative + text[len(non_imperative):]
                    break

        return text

    def generate_function_signature(self, api: Dict[str, Any]) -> str:
        """Generate Python function signature."""
        api_name = api["name"]

        # Remove module prefix (e.g., "card.", "var.") and convert to camelCase
        parts = api_name.split('.', 1)
        if len(parts) > 1:
            func_name = self.to_camel_case(parts[1])  # Convert remaining parts to camelCase
        else:
            func_name = self.to_camel_case(api_name)

        params = ["card"]

        # Add parameters based on properties
        properties = api["properties"]
        required = api["required"]

        # Separate required and optional parameters
        required_params = []
        optional_params = []

        # Add parameters for schema properties
        for prop_name, _ in properties.items():
            if prop_name in ["req", "cmd"]:  # Skip these as they're auto-generated
                continue

            # Handle reserved keywords by appending underscore
            param_name = prop_name
            if param_name in self.reserved_keywords:
                param_name = f"{param_name}_"

            # Separate required and optional parameters
            if prop_name in required and prop_name not in ["req", "cmd"]:
                required_params.append(f"{param_name}")
            else:
                optional_params.append(f"{param_name}=None")

        # Add required parameters first, then optional parameters
        params.extend(required_params)
        params.extend(optional_params)


        return f"def {func_name}({', '.join(params)}):"

    def _build_docstring_content(self, api: Dict[str, Any], imperative_description: str) -> str:
        """Build complete docstring content to check for backslashes."""
        lines = [imperative_description, ""]

        properties = api["properties"]

        # Process schema properties
        for prop_name, prop_def in properties.items():
            if prop_name in ["req", "cmd"]:
                continue

            # Handle reserved keywords by appending underscore for parameter name
            param_name = prop_name
            if param_name in self.reserved_keywords:
                param_name = f"{param_name}_"

            prop_desc = self.clean_docstring_text(prop_def.get("description", f"The {prop_name} parameter."))
            lines.append(f"        {param_name} (type): {prop_desc}")

        return "\n".join(lines)

    def generate_docstring(self, api: Dict[str, Any]) -> str:
        """Generate function docstring."""
        # Clean the description text
        clean_description = self.clean_docstring_text(api["description"])
        # Convert to imperative mood (Pydocstyle D402)
        imperative_description = self.convert_to_imperative_mood(clean_description)

        # Check if docstring contains backslashes and use raw string if needed
        docstring_content = self._build_docstring_content(api, imperative_description)
        has_backslashes = '\\' in docstring_content

        if has_backslashes:
            lines = [f'    r"""{imperative_description}']
        else:
            lines = [f'    """{imperative_description}']
        lines.append("")
        lines.append("    Args:")
        lines.append("        card (Notecard): The current Notecard object.")

        properties = api["properties"]

        # Process schema properties
        for prop_name, prop_def in properties.items():
            if prop_name in ["req", "cmd"]:
                continue

            # Handle reserved keywords by appending underscore for parameter name
            param_name = prop_name
            if param_name in self.reserved_keywords:
                param_name = f"{param_name}_"

            prop_type = self.get_python_type_hint(prop_def)
            prop_desc = self.clean_docstring_text(prop_def.get("description", f"The {prop_name} parameter."))
            lines.append(f"        {param_name} ({prop_type}): {prop_desc}")


        lines.append("")
        lines.append("    Returns:")
        lines.append("        dict: The result of the Notecard request.")
        lines.append('    """')

        return "\n".join(lines)

    def generate_function_body(self, api: Dict[str, Any]) -> str:
        """Generate function body."""
        api_name = api["name"]
        lines = [f'    req = {{"req": "{api_name}"}}']

        properties = api["properties"]

        # Process schema properties
        for prop_name, prop_def in properties.items():
            if prop_name in ["req", "cmd"]:
                continue

            # Handle reserved keywords by appending underscore for parameter name
            param_name = prop_name
            if param_name in self.reserved_keywords:
                param_name = f"{param_name}_"

            json_type = prop_def.get("type", "string")

            # Handle case where type is a list of types
            if isinstance(json_type, list):
                # Use the first non-null type
                for t in json_type:
                    if t != "null":
                        json_type = t
                        break
                else:
                    json_type = "string"

            # Use 'is not None' for types that can have falsy but valid values (0, False, "", etc.)
            if json_type in ["boolean", "integer", "number"]:
                lines.append(f"    if {param_name} is not None:")
                lines.append(f'        req["{prop_name}"] = {param_name}')
            else:
                lines.append(f"    if {param_name}:")
                lines.append(f'        req["{prop_name}"] = {param_name}')


        lines.append("    return card.Transaction(req)")

        return "\n".join(lines)

    def generate_api_function(self, api: Dict[str, Any]) -> str:
        """Generate complete API function."""
        lines = []
        lines.append("")
        lines.append("")
        lines.append("@validate_card_object")
        lines.append(self.generate_function_signature(api))
        lines.append(self.generate_docstring(api))
        lines.append(self.generate_function_body(api))

        return "\n".join(lines)

    def group_apis_by_module(self, apis: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group APIs by their module (first part of the name)."""
        modules = {}

        for api in apis:
            module_name = api["name"].split(".")[0]
            if module_name not in modules:
                modules[module_name] = []
            modules[module_name].append(api)

        return modules

    def generate_module_file(self, module_name: str, apis: List[Dict[str, Any]]) -> str:
        """Generate complete module file content."""
        lines = [f'"""{module_name} Fluent API Helper."""']
        lines.append("")
        lines.append("##")
        lines.append(f"# @file {module_name}.py")
        lines.append("#")
        lines.append(f"# @brief {module_name} Fluent API Helper.")
        lines.append("#")
        lines.append("# @section description Description")
        lines.append(f"# This module contains helper methods for calling {module_name}.* Notecard API commands.")
        lines.append("# This module is optional and not required for use with the Notecard.")
        lines.append("")
        lines.append("from notecard.validators import validate_card_object")

        for api in apis:
            lines.append(self.generate_api_function(api))

        # Ensure the file ends with a newline
        return "\n".join(lines) + "\n"

    def generate_all_apis(self, output_dir: str = "notecard"):
        """Generate all API modules."""
        print("Fetching main schema...")
        refs = self.parse_main_schema()

        if not refs:
            print("No API references found in main schema")
            return

        print(f"Found {len(refs)} API references")

        # Parse all API schemas
        apis = []
        for ref in refs:
            print(f"Processing {ref}...")
            api = self.parse_api_schema(ref)
            if api:
                apis.append(api)

        print(f"Successfully parsed {len(apis)} APIs")

        # Group by module
        modules = self.group_apis_by_module(apis)

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        for module_name, module_apis in modules.items():
            print(f"Generating {module_name}.py with {len(module_apis)} APIs...")

            file_content = self.generate_module_file(module_name, module_apis)

            file_path = output_path / f"{module_name}.py"
            with open(file_path, "w") as f:
                f.write(file_content)

            print(f"Generated {file_path}")

        print(f"\nGeneration complete! Generated {len(modules)} modules with {len(apis)} total APIs.")
        print(f"Files created in: {output_path.absolute()}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate Notecard API functions from JSON schema")
    parser.add_argument(
        "--output-dir",
        default="generated_apis",
        help="Output directory for generated API files (default: generated_apis)"
    )
    parser.add_argument(
        "--schema-url",
        default="https://raw.githubusercontent.com/blues/notecard-schema/refs/heads/master/notecard.api.json",
        help="URL to the main Notecard API schema"
    )

    args = parser.parse_args()

    generator = NotecardAPIGenerator(args.schema_url)
    generator.generate_all_apis(args.output_dir)


if __name__ == "__main__":
    main()
