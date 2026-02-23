import sys
from pathlib import Path

def define_ast(output_dir, base_name, types):
    file_path = Path(f"{output_dir}/{base_name}.py")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("from abc import ABC, abstractmethod\n"
                   "from dataclasses import dataclass\n"
                   "from typing import Any\n"
                   "from lox_token import Token\n\n")
        define_visitor(file, base_name, types)
        file.write(f"class {base_name}(ABC):\n")
        file.write(f"    @abstractmethod\n")
        file.write(f"    def accept(self, visitor: Visitor) -> Any:\n")
        file.write(f"        pass\n\n")


        for typ in types:
            class_name = typ.split(":")[0].strip()
            fields = typ.split(":")[1].strip()
            define_type(file, base_name, class_name, fields)

def define_type(file, base_name, class_name, field_list):
    file.write("@dataclass(frozen=True)\n")
    file.write(f"class {class_name}({base_name}):\n")

    fields = [f.strip() for f in field_list.split(",")]
    for field in fields:
        name = field.split(" ")[0]
        typ = field.split(" ")[1]
        file.write(f"    {name}: {typ}\n")
    file.write("\n")
    file.write(f"    def accept(self, visitor: Visitor) -> Any:\n")
    file.write(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n\n")

def define_visitor(file, base_name, types):
    file.write(f"class Visitor(ABC):\n")
    for typ in types:
        class_name = typ.split(":")[0].strip()
        file.write(f"    @abstractmethod\n")
        file.write(f"    def visit_{class_name.lower()}_{base_name.lower()}(self, {base_name.lower()}: '{class_name}') -> Any:\n")
        file.write(f"        pass\n\n")


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)
    else:
        output_dir = args[0]
        base_name = "Expr"
        types = ["Binary   : left Expr, operator Token, right Expr",
                 "Grouping : expression Expr",
                 "Literal  : value Any",
                 "Unary    : operator Token, right Expr"]
        
        define_ast(output_dir, base_name, types)

if __name__ == "__main__": 
    main()
