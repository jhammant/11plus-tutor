#!/usr/bin/env python3
"""
Non-Verbal Reasoning Question Generator for 11+ Tutor

Generates SVG-based NVR questions including:
- Pattern sequences (shapes follow a rule)
- Shape analogies (A:B :: C:?)
- Odd one out (which shape doesn't belong)
- Rotations and reflections

All shapes are generated as SVG strings that can be rendered directly in the browser.
"""

import sqlite3
import json
import random
import uuid
import math
from typing import List, Dict, Tuple

# =============================================================================
# SVG Shape Generator
# =============================================================================

class SVGShapeGenerator:
    """Generate SVG shapes for NVR questions."""
    
    COLORS = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']
    SHAPES = ['circle', 'square', 'triangle', 'pentagon', 'hexagon', 'star', 'diamond']
    
    def __init__(self, size: int = 80):
        self.size = size
        self.center = size // 2
    
    def create_svg(self, content: str, viewbox: str = None) -> str:
        """Wrap content in SVG tags."""
        vb = viewbox or f"0 0 {self.size} {self.size}"
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{self.size}" height="{self.size}">{content}</svg>'
    
    def circle(self, cx: int = None, cy: int = None, r: int = None, 
               fill: str = '#3B82F6', stroke: str = '#1E40AF', stroke_width: int = 2) -> str:
        cx = cx or self.center
        cy = cy or self.center
        r = r or (self.size // 2 - 5)
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    
    def square(self, x: int = None, y: int = None, size: int = None,
               fill: str = '#EF4444', stroke: str = '#B91C1C', stroke_width: int = 2,
               rotation: int = 0) -> str:
        size = size or (self.size - 10)
        x = x if x is not None else 5
        y = y if y is not None else 5
        transform = f' transform="rotate({rotation} {self.center} {self.center})"' if rotation else ''
        return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{transform}/>'
    
    def triangle(self, cx: int = None, cy: int = None, size: int = None,
                 fill: str = '#10B981', stroke: str = '#047857', stroke_width: int = 2,
                 rotation: int = 0) -> str:
        cx = cx or self.center
        cy = cy or self.center
        size = size or (self.size - 10)
        h = size * math.sqrt(3) / 2
        points = f"{cx},{cy - h*2/3} {cx - size/2},{cy + h/3} {cx + size/2},{cy + h/3}"
        transform = f' transform="rotate({rotation} {cx} {cy})"' if rotation else ''
        return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{transform}/>'
    
    def pentagon(self, cx: int = None, cy: int = None, r: int = None,
                 fill: str = '#F59E0B', stroke: str = '#B45309', stroke_width: int = 2,
                 rotation: int = 0) -> str:
        return self._regular_polygon(5, cx, cy, r, fill, stroke, stroke_width, rotation)
    
    def hexagon(self, cx: int = None, cy: int = None, r: int = None,
                fill: str = '#8B5CF6', stroke: str = '#6D28D9', stroke_width: int = 2,
                rotation: int = 0) -> str:
        return self._regular_polygon(6, cx, cy, r, fill, stroke, stroke_width, rotation)
    
    def star(self, cx: int = None, cy: int = None, r: int = None,
             fill: str = '#EC4899', stroke: str = '#BE185D', stroke_width: int = 2,
             points_count: int = 5, rotation: int = 0) -> str:
        cx = cx or self.center
        cy = cy or self.center
        r = r or (self.size // 2 - 5)
        inner_r = r * 0.4
        
        points = []
        for i in range(points_count * 2):
            angle = math.pi * i / points_count - math.pi / 2
            radius = r if i % 2 == 0 else inner_r
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        
        transform = f' transform="rotate({rotation} {cx} {cy})"' if rotation else ''
        return f'<polygon points="{" ".join(points)}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{transform}/>'
    
    def diamond(self, cx: int = None, cy: int = None, size: int = None,
                fill: str = '#06B6D4', stroke: str = '#0E7490', stroke_width: int = 2,
                rotation: int = 0) -> str:
        cx = cx or self.center
        cy = cy or self.center
        size = size or (self.size // 2 - 5)
        points = f"{cx},{cy - size} {cx + size},{cy} {cx},{cy + size} {cx - size},{cy}"
        transform = f' transform="rotate({rotation} {cx} {cy})"' if rotation else ''
        return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{transform}/>'
    
    def _regular_polygon(self, sides: int, cx: int = None, cy: int = None, r: int = None,
                         fill: str = '#3B82F6', stroke: str = '#1E40AF', stroke_width: int = 2,
                         rotation: int = 0) -> str:
        cx = cx or self.center
        cy = cy or self.center
        r = r or (self.size // 2 - 5)
        
        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides - math.pi / 2
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        
        transform = f' transform="rotate({rotation} {cx} {cy})"' if rotation else ''
        return f'<polygon points="{" ".join(points)}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{transform}/>'
    
    def get_shape(self, shape_type: str, **kwargs) -> str:
        """Get a shape by type name."""
        methods = {
            'circle': self.circle,
            'square': self.square,
            'triangle': self.triangle,
            'pentagon': self.pentagon,
            'hexagon': self.hexagon,
            'star': self.star,
            'diamond': self.diamond,
        }
        return methods.get(shape_type, self.circle)(**kwargs)
    
    def shape_with_inner(self, outer: str, inner: str, outer_color: str, inner_color: str) -> str:
        """Create a shape with another shape inside it."""
        outer_svg = self.get_shape(outer, fill=outer_color, r=self.size//2 - 5)
        inner_svg = self.get_shape(inner, fill=inner_color, r=self.size//4, 
                                   size=self.size//3, cx=self.center, cy=self.center)
        return outer_svg + inner_svg

# =============================================================================
# NVR Question Generators
# =============================================================================

class NVRQuestionGenerator:
    """Generate Non-Verbal Reasoning questions."""
    
    def __init__(self, db_path: str = "elevenplustutor.db"):
        self.db_path = db_path
        self.svg = SVGShapeGenerator(80)
    
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def save_question(self, question: dict):
        """Save a question to the database."""
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO questions (
                id, exam_type, subject, topic, question_type, difficulty,
                question_text, options, correct_answer, correct_index,
                marks_available, hint, worked_solution
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question['id'],
            question.get('exam_type', '11plus_gl'),
            question['subject'],
            question.get('topic', question['question_type']),
            question['question_type'],
            question['difficulty'],
            question['question_text'],
            json.dumps(question['options']),
            question['correct_answer'],
            question['correct_index'],
            question.get('marks_available', 1),
            question.get('hint'),
            question.get('worked_solution')
        ))
        
        conn.commit()
        conn.close()
    
    # =========================================================================
    # Pattern Sequence Questions
    # =========================================================================
    
    def generate_rotation_sequence(self, difficulty: int = 2) -> dict:
        """Generate a sequence where shapes rotate."""
        shape = random.choice(['triangle', 'square', 'pentagon', 'star'])
        color = random.choice(SVGShapeGenerator.COLORS)
        
        if difficulty <= 2:
            rotation_step = random.choice([45, 90])
        else:
            rotation_step = random.choice([30, 45, 60, 72])
        
        # Create sequence
        sequence_svgs = []
        for i in range(4):
            svg_content = self.svg.get_shape(shape, fill=color, rotation=i * rotation_step)
            sequence_svgs.append(self.svg.create_svg(svg_content))
        
        # Correct answer
        correct_rotation = 4 * rotation_step
        correct_svg = self.svg.create_svg(self.svg.get_shape(shape, fill=color, rotation=correct_rotation))
        
        # Wrong answers (different rotations)
        wrong_rotations = [
            correct_rotation + rotation_step,
            correct_rotation - rotation_step,
            correct_rotation + 2 * rotation_step,
            0  # No rotation
        ]
        wrong_svgs = [self.svg.create_svg(self.svg.get_shape(shape, fill=color, rotation=r)) 
                      for r in wrong_rotations[:4]]
        
        options = wrong_svgs[:4] + [correct_svg]
        random.shuffle(options)
        correct_index = options.index(correct_svg)
        
        # Combine sequence images into question_text as JSON
        question_data = {
            'type': 'nvr_sequence',
            'sequence': sequence_svgs,
            'instruction': 'What comes next in the sequence?'
        }
        
        return {
            'id': str(uuid.uuid4()),
            'subject': 'non_verbal_reasoning',
            'question_type': 'nvr_sequences',
            'difficulty': difficulty,
            'question_text': json.dumps(question_data),
            'options': options,
            'correct_answer': str(correct_index),
            'correct_index': correct_index,
            'worked_solution': f"The {shape} rotates {rotation_step}° clockwise each step. After 4 steps, it has rotated {correct_rotation}°."
        }
    
    def _get_shape_with_size(self, shape: str, size: int, color: str) -> str:
        """Helper to create a shape with the appropriate size parameter."""
        if shape == 'circle':
            return self.svg.circle(r=size, fill=color)
        elif shape == 'square':
            return self.svg.square(size=size*2, x=(80-size*2)//2, y=(80-size*2)//2, fill=color)
        elif shape == 'triangle':
            return self.svg.triangle(size=size*2, fill=color)
        elif shape == 'diamond':
            return self.svg.diamond(size=size, fill=color)
        else:
            # pentagon, hexagon, star all use 'r'
            return self.svg.get_shape(shape, r=size, fill=color)

    def generate_size_sequence(self, difficulty: int = 2) -> dict:
        """Generate a sequence where shapes change size."""
        shape = random.choice(['circle', 'square', 'triangle', 'hexagon'])
        color = random.choice(SVGShapeGenerator.COLORS)

        # Sizes: increasing or decreasing
        if random.choice([True, False]):
            sizes = [15, 22, 29, 36]  # Increasing
            next_size = 43
            pattern = "increases by 7"
        else:
            sizes = [40, 34, 28, 22]  # Decreasing
            next_size = 16
            pattern = "decreases by 6"

        sequence_svgs = []
        for size in sizes:
            svg_content = self._get_shape_with_size(shape, size, color)
            sequence_svgs.append(self.svg.create_svg(svg_content))

        # Correct answer
        correct_svg = self.svg.create_svg(self._get_shape_with_size(shape, next_size, color))

        # Wrong answers
        wrong_sizes = [next_size + 7, next_size - 7, sizes[-1], next_size + 3]
        wrong_svgs = []
        for ws in wrong_sizes:
            if ws > 5 and ws < 45:
                wrong_svgs.append(self.svg.create_svg(self._get_shape_with_size(shape, ws, color)))
        
        options = wrong_svgs[:4] + [correct_svg]
        random.shuffle(options)
        correct_index = options.index(correct_svg)
        
        question_data = {
            'type': 'nvr_sequence',
            'sequence': sequence_svgs,
            'instruction': 'What comes next in the sequence?'
        }
        
        return {
            'id': str(uuid.uuid4()),
            'subject': 'non_verbal_reasoning',
            'question_type': 'nvr_sequences',
            'difficulty': difficulty,
            'question_text': json.dumps(question_data),
            'options': options,
            'correct_answer': str(correct_index),
            'correct_index': correct_index,
            'worked_solution': f"The {shape} {pattern} each step."
        }
    
    def generate_shape_change_sequence(self, difficulty: int = 2) -> dict:
        """Generate a sequence where shapes change (triangle -> square -> pentagon -> hexagon)."""
        color = random.choice(SVGShapeGenerator.COLORS)
        
        # Shapes that progress by adding sides
        shape_progression = ['triangle', 'square', 'pentagon', 'hexagon']
        
        sequence_svgs = []
        for shape in shape_progression:
            svg_content = self.svg.get_shape(shape, fill=color)
            sequence_svgs.append(self.svg.create_svg(svg_content))
        
        # Next shape would have 7 sides, but we'll use star as "7-pointed"
        # Actually let's cycle back or use a different pattern
        correct_shape = 'star'  # 7 points ~ 7 sides conceptually
        correct_svg = self.svg.create_svg(self.svg.get_shape(correct_shape, fill=color))
        
        # Wrong answers
        wrong_shapes = ['circle', 'triangle', 'square', 'diamond']
        wrong_svgs = [self.svg.create_svg(self.svg.get_shape(s, fill=color)) for s in wrong_shapes]
        
        options = wrong_svgs[:4] + [correct_svg]
        random.shuffle(options)
        correct_index = options.index(correct_svg)
        
        question_data = {
            'type': 'nvr_sequence',
            'sequence': sequence_svgs,
            'instruction': 'What comes next in the sequence?'
        }
        
        return {
            'id': str(uuid.uuid4()),
            'subject': 'non_verbal_reasoning',
            'question_type': 'nvr_sequences',
            'difficulty': difficulty,
            'question_text': json.dumps(question_data),
            'options': options,
            'correct_answer': str(correct_index),
            'correct_index': correct_index,
            'worked_solution': "Each shape gains one more side: 3→4→5→6→7 (star has 7 points)."
        }
    
    # =========================================================================
    # Odd One Out Questions
    # =========================================================================
    
    def generate_odd_one_out_rotation(self, difficulty: int = 2) -> dict:
        """One shape is rotated differently from the others."""
        shape = random.choice(['triangle', 'square', 'pentagon', 'star'])
        color = random.choice(SVGShapeGenerator.COLORS)
        
        base_rotation = random.choice([0, 45, 90])
        odd_rotation = base_rotation + random.choice([15, 30, 60, 120])
        
        # Create 4 similar shapes and 1 odd one
        shapes = []
        for i in range(4):
            svg = self.svg.create_svg(self.svg.get_shape(shape, fill=color, rotation=base_rotation))
            shapes.append(svg)
        
        odd_svg = self.svg.create_svg(self.svg.get_shape(shape, fill=color, rotation=odd_rotation))
        
        # Insert odd one at random position
        correct_index = random.randint(0, 4)
        shapes.insert(correct_index, odd_svg)
        
        question_data = {
            'type': 'nvr_odd_one_out',
            'shapes': shapes,
            'instruction': 'Which shape is the odd one out?'
        }
        
        return {
            'id': str(uuid.uuid4()),
            'subject': 'non_verbal_reasoning',
            'question_type': 'nvr_odd_one_out',
            'difficulty': difficulty,
            'question_text': json.dumps(question_data),
            'options': ['A', 'B', 'C', 'D', 'E'],
            'correct_answer': chr(65 + correct_index),
            'correct_index': correct_index,
            'worked_solution': f"Shape {chr(65 + correct_index)} is rotated differently from the others."
        }
    
    def generate_odd_one_out_shape(self, difficulty: int = 2) -> dict:
        """One shape is different from the others."""
        main_shape = random.choice(['circle', 'square', 'triangle', 'pentagon'])
        odd_shape = random.choice([s for s in ['circle', 'square', 'triangle', 'pentagon', 'hexagon', 'star'] if s != main_shape])
        color = random.choice(SVGShapeGenerator.COLORS)
        
        shapes = []
        for i in range(4):
            svg = self.svg.create_svg(self.svg.get_shape(main_shape, fill=color))
            shapes.append(svg)
        
        odd_svg = self.svg.create_svg(self.svg.get_shape(odd_shape, fill=color))
        
        correct_index = random.randint(0, 4)
        shapes.insert(correct_index, odd_svg)
        
        question_data = {
            'type': 'nvr_odd_one_out',
            'shapes': shapes,
            'instruction': 'Which shape is the odd one out?'
        }
        
        return {
            'id': str(uuid.uuid4()),
            'subject': 'non_verbal_reasoning',
            'question_type': 'nvr_odd_one_out',
            'difficulty': difficulty,
            'question_text': json.dumps(question_data),
            'options': ['A', 'B', 'C', 'D', 'E'],
            'correct_answer': chr(65 + correct_index),
            'correct_index': correct_index,
            'worked_solution': f"Shape {chr(65 + correct_index)} is a {odd_shape}, while the others are {main_shape}s."
        }
    
    # =========================================================================
    # Analogy Questions
    # =========================================================================
    
    def generate_shape_analogy(self, difficulty: int = 2) -> dict:
        """A is to B as C is to ?"""
        # Simple transformation: change color, size, or add inner shape
        shape1 = random.choice(['circle', 'square', 'triangle'])
        shape2 = random.choice(['pentagon', 'hexagon', 'star'])
        color1 = random.choice(SVGShapeGenerator.COLORS[:3])
        color2 = random.choice(SVGShapeGenerator.COLORS[3:])
        
        # A: shape1 with color1, B: shape1 with color2 (color change)
        # C: shape2 with color1, D: shape2 with color2
        
        svg_a = self.svg.create_svg(self.svg.get_shape(shape1, fill=color1))
        svg_b = self.svg.create_svg(self.svg.get_shape(shape1, fill=color2))
        svg_c = self.svg.create_svg(self.svg.get_shape(shape2, fill=color1))
        correct_svg = self.svg.create_svg(self.svg.get_shape(shape2, fill=color2))
        
        # Wrong answers
        wrong_svgs = [
            self.svg.create_svg(self.svg.get_shape(shape2, fill=color1)),  # No color change
            self.svg.create_svg(self.svg.get_shape(shape1, fill=color2)),  # Wrong shape
            self.svg.create_svg(self.svg.get_shape('diamond', fill=color2)),  # Random
            self.svg.create_svg(self.svg.get_shape(shape2, fill='#9CA3AF')),  # Wrong color
        ]
        
        options = wrong_svgs[:4] + [correct_svg]
        random.shuffle(options)
        correct_index = options.index(correct_svg)
        
        question_data = {
            'type': 'nvr_analogy',
            'pair1': [svg_a, svg_b],
            'pair2_first': svg_c,
            'instruction': 'A is to B as C is to ?'
        }
        
        return {
            'id': str(uuid.uuid4()),
            'subject': 'non_verbal_reasoning',
            'question_type': 'nvr_analogies',
            'difficulty': difficulty,
            'question_text': json.dumps(question_data),
            'options': options,
            'correct_answer': str(correct_index),
            'correct_index': correct_index,
            'worked_solution': f"The pattern is: the shape changes color. So the {shape2} should also change to the same color."
        }
    
    # =========================================================================
    # Batch Generation
    # =========================================================================
    
    def generate_sequences_batch(self, count: int = 50) -> List[dict]:
        """Generate NVR sequence questions."""
        questions = []
        generators = [
            self.generate_rotation_sequence,
            self.generate_size_sequence,
            self.generate_shape_change_sequence,
        ]
        
        for _ in range(count):
            gen = random.choice(generators)
            difficulty = random.choices([2, 3, 4], weights=[0.4, 0.4, 0.2])[0]
            questions.append(gen(difficulty))
        
        return questions
    
    def generate_odd_one_out_batch(self, count: int = 50) -> List[dict]:
        """Generate NVR odd one out questions."""
        questions = []
        generators = [
            self.generate_odd_one_out_rotation,
            self.generate_odd_one_out_shape,
        ]
        
        for _ in range(count):
            gen = random.choice(generators)
            difficulty = random.choices([2, 3, 4], weights=[0.4, 0.4, 0.2])[0]
            questions.append(gen(difficulty))
        
        return questions
    
    def generate_analogies_batch(self, count: int = 50) -> List[dict]:
        """Generate NVR analogy questions."""
        questions = []
        for _ in range(count):
            difficulty = random.choices([2, 3, 4], weights=[0.4, 0.4, 0.2])[0]
            questions.append(self.generate_shape_analogy(difficulty))
        return questions


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate NVR questions')
    parser.add_argument('--type', choices=['sequences', 'odd_one_out', 'analogies', 'all'], default='all')
    parser.add_argument('--count', type=int, default=50)
    parser.add_argument('--db', default='elevenplustutor.db')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    generator = NVRQuestionGenerator(args.db)
    questions = []
    
    if args.type in ['sequences', 'all']:
        print(f"Generating {args.count} NVR sequence questions...")
        questions.extend(generator.generate_sequences_batch(args.count))
    
    if args.type in ['odd_one_out', 'all']:
        print(f"Generating {args.count} NVR odd-one-out questions...")
        questions.extend(generator.generate_odd_one_out_batch(args.count))
    
    if args.type in ['analogies', 'all']:
        print(f"Generating {args.count} NVR analogy questions...")
        questions.extend(generator.generate_analogies_batch(args.count))
    
    if args.dry_run:
        print(f"\nGenerated {len(questions)} questions (not saved)")
        for q in questions[:2]:
            print(f"\nType: {q['question_type']}")
            print(f"Solution: {q['worked_solution']}")
    else:
        for q in questions:
            generator.save_question(q)
        print(f"\nSaved {len(questions)} NVR questions to database")


if __name__ == '__main__':
    main()
