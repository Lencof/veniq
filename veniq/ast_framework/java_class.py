from cached_property import cached_property  # type: ignore
from deprecated import deprecated  # type: ignore

from typing import Dict, Set, TYPE_CHECKING
from networkx import DiGraph  # type: ignore

from veniq.ast_framework import AST, ASTNodeType
from veniq.ast_framework.java_class_method import JavaClassMethod
from veniq.ast_framework.java_class_field import JavaClassField

if TYPE_CHECKING:
    from veniq.ast_framework.java_package import JavaPackage


@deprecated("This functionality must be transmitted to ASTNode")
class JavaClass(AST):
    def __init__(self, tree: DiGraph, root: int, java_package: 'JavaPackage'):
        self.tree = tree
        self.root = root
        self._java_package = java_package

    @cached_property
    def name(self) -> str:
        try:
            class_name = next(self.children_with_type(self.root, ASTNodeType.STRING))
            return self.tree.nodes[class_name]['string']
        except StopIteration:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def package(self) -> 'JavaPackage':
        return self._java_package

    @cached_property
    def methods(self) -> Dict[str, Set[JavaClassMethod]]:
        methods: Dict[str, Set[JavaClassMethod]] = {}
        for method_ast in self.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            method = JavaClassMethod(method_ast.tree, method_ast.root, self)
            if method.name in methods:
                methods[method.name].add(method)
            else:
                methods[method.name] = {method}
        return methods

    @cached_property
    def fields(self) -> Dict[str, JavaClassField]:
        fields: Dict[str, JavaClassField] = {}
        for field_ast in self.get_subtrees(ASTNodeType.FIELD_DECLARATION):
            field = JavaClassField(field_ast.tree, field_ast.root, self)
            fields[field.name] = field
        return fields
