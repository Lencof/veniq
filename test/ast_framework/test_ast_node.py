from unittest import TestCase
from pathlib import Path

from veniq.ast_framework import AST, ASTNodeType
from veniq.utils.ast_builder import build_ast
import os # use os
import sys # use sys

# create class ASTNodeTestSuite(TestCase):
class ASTNodeTestSuite(TestCase):
    def test_class_computed_fields(self):
        ast = AST.build_from_javalang(
            build_ast(
                Path(__file__).absolute().parent / "MethodUseOtherMethodExample.java"
            )
        )
        package = ast.get_root()
        assert len(package.types) == 1 and \
            package.types[0].node_type == ASTNodeType.CLASS_DECLARATION

        java_class = package.types[0]
        self.assertEqual(java_class.name, "MethodUseOtherMethod")
        self.assertEqual(java_class.modifiers, set())
        self.assertEqual(java_class.documentation, "/**\n* Some documentation\n*/")

        # consider each field declaration declares single field
        fields_names = {field.names[0] for field in java_class.fields}
        self.assertEqual(fields_names, {"connectingField", "redundantField"})

        methods_names = {method.name for method in java_class.methods}
        self.assertEqual(
            methods_names,
            {
                "useOnlyMethods1",
                "useOnlyMethods2",
                "getField",
                "setField",
                "standAloneMethod",
                "shadowing",
            },
        )

        self.assertEqual(set(java_class.constructors), set())

    # create def test_fake_node(self):   
    def test_fake_node(self):
        ast = AST.build_from_javalang(
            build_ast(
                Path(__file__).absolute().parent / "MethodUseOtherMethodExample.java"
            )
        )

        fake_node = ast.create_fake_node()

        # fixed public interface
        self.assertTrue(fake_node.is_fake)
        self.assertEqual(list(fake_node.children), [])
        self.assertEqual(fake_node.line, -1)
        self.assertEqual(fake_node.parent, None)
        self.assertEqual(fake_node.node_index, -1)

        # proxy interface
        self.assertEqual(fake_node.node_type, None)

        # interface through standart python function
        self.assertEqual(str(fake_node),
                         "node index: -1\n"
                         "node_type: None")
        self.assertEqual(repr(fake_node), "<ASTNode node_type: None, node_index: -1>")
        self.assertEqual(dir(fake_node), ["children", "is_fake", "line", "node_index", "parent"])

        try:
            hash(fake_node)
        except Exception as e:
            self.fail(f"Failed to hash fake node with following exception {e}.")

    # create def test_fake_nodes_equality(self):        
    def test_fake_nodes_equality(self):
        ast1 = AST.build_from_javalang(
            build_ast(
                Path(__file__).absolute().parent / "MethodUseOtherMethodExample.java"
            )
        )

        ast2 = AST.build_from_javalang(
            build_ast(
                Path(__file__).absolute().parent / "LottieImageAsset.java"
            )
        )

        ast1_fake_node1 = ast1.create_fake_node()
        ast1_fake_node2 = ast1.create_fake_node()
        ast2_fake_node1 = ast2.create_fake_node()

        self.assertFalse(ast1_fake_node1 == ast1_fake_node2)
        self.assertFalse(ast1_fake_node1 == ast2_fake_node1)
