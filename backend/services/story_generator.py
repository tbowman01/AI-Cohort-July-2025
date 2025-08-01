"""
Story Generation Service for AutoDevHub

This service converts natural language feature descriptions into structured
Gherkin user stories using template-based generation for reliable demo
functionality.
"""

import re
import logging
from typing import Dict, List, Tuple
from datetime import datetime
from enum import Enum


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StoryType(Enum):
    """Supported story types"""
    EPIC = "epic"
    FEATURE = "feature"
    STORY = "story"
    TASK = "task"


class Priority(Enum):
    """Story priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StoryTemplate:
    """Template patterns for generating Gherkin stories"""

    # Common user roles detected from feature descriptions
    USER_ROLES = {
        'auth': 'user',
        'login': 'user',
        'register': 'user',
        'profile': 'user',
        'account': 'user',
        'admin': 'administrator',
        'manage': 'administrator',
        'dashboard': 'user',
        'api': 'developer',
        'data': 'analyst',
        'report': 'manager',
        'payment': 'customer',
        'order': 'customer',
        'notification': 'user',
        'search': 'user',
        'chat': 'user',
        'message': 'user',
        'file': 'user',
        'upload': 'user',
        'download': 'user'
    }

    # Template patterns for different feature types
    FEATURE_PATTERNS = {
        'authentication': {
            'keywords': ['auth', 'login', 'register', 'sign', 'password', 'token'],
            'template': {
                'feature': 'User Authentication',
                'user_story': 'As a {role}\nI want to {action}\nSo that I can {benefit}',
                'scenarios': [
                    {
                        'name': 'Successful authentication',
                        'given': 'I am on the login page',
                        'when': 'I enter valid credentials',
                        'then': 'I should be logged in successfully'
                    },
                    {
                        'name': 'Invalid credentials',
                        'given': 'I am on the login page',
                        'when': 'I enter invalid credentials',
                        'then': 'I should see an error message'
                    }
                ]
            }
        },
        'crud': {
            'keywords': ['create', 'add', 'edit', 'update', 'delete', 'remove', 'manage'],
            'template': {
                'feature': 'Data Management',
                'user_story': 'As a {role}\nI want to {action}\nSo that I can {benefit}',
                'scenarios': [
                    {
                        'name': 'Create new item',
                        'given': 'I am on the management page',
                        'when': 'I create a new item with valid information',
                        'then': 'the item should be saved successfully'
                    },
                    {
                        'name': 'Update existing item',
                        'given': 'I have an existing item',
                        'when': 'I update the item information',
                        'then': 'the changes should be saved'
                    }
                ]
            }
        },
        'api': {
            'keywords': ['api', 'endpoint', 'service', 'rest', 'graphql'],
            'template': {
                'feature': 'API Integration',
                'user_story': 'As a {role}\nI want to {action}\nSo that I can {benefit}',
                'scenarios': [
                    {
                        'name': 'Successful API call',
                        'given': 'the API is available',
                        'when': 'I make a valid API request',
                        'then': 'I should receive the correct response'
                    },
                    {
                        'name': 'Handle API errors',
                        'given': 'the API is unavailable',
                        'when': 'I make an API request',
                        'then': 'I should receive an appropriate error message'
                    }
                ]
            }
        },
        'search': {
            'keywords': ['search', 'find', 'filter', 'query', 'lookup'],
            'template': {
                'feature': 'Search Functionality',
                'user_story': 'As a {role}\nI want to {action}\nSo that I can {benefit}',
                'scenarios': [
                    {
                        'name': 'Successful search',
                        'given': 'I am on the search page',
                        'when': 'I enter a search term and click search',
                        'then': 'I should see relevant results'
                    },
                    {
                        'name': 'No search results',
                        'given': 'I am on the search page',
                        'when': 'I search for a term with no matches',
                        'then': 'I should see a no results message'
                    }
                ]
            }
        },
        'file_management': {
            'keywords': ['file', 'upload', 'download', 'attach', 'document'],
            'template': {
                'feature': 'File Management',
                'user_story': 'As a {role}\nI want to {action}\nSo that I can {benefit}',
                'scenarios': [
                    {
                        'name': 'Upload file successfully',
                        'given': 'I am on the file upload page',
                        'when': 'I select and upload a valid file',
                        'then': 'the file should be uploaded successfully'
                    },
                    {
                        'name': 'Invalid file type',
                        'given': 'I am on the file upload page',
                        'when': 'I try to upload an invalid file type',
                        'then': 'I should see an error message'
                    }
                ]
            }
        },
        'notification': {
            'keywords': ['notification', 'alert', 'message', 'email', 'notify'],
            'template': {
                'feature': 'Notification System',
                'user_story': 'As a {role}\nI want to {action}\nSo that I can {benefit}',
                'scenarios': [
                    {
                        'name': 'Receive notification',
                        'given': 'I have notifications enabled',
                        'when': 'an event occurs that requires notification',
                        'then': 'I should receive a notification'
                    },
                    {
                        'name': 'Mark notification as read',
                        'given': 'I have unread notifications',
                        'when': 'I click on a notification',
                        'then': 'it should be marked as read'
                    }
                ]
            }
        }
    }


class StoryGenerator:
    """Main service class for generating Gherkin user stories"""

    def __init__(self):
        """Initialize the story generator with templates"""
        self.templates = StoryTemplate()
        logger.info("StoryGenerator initialized with template-based generation")

    def generate_gherkin_story(
        self,
        feature_description: str,
        story_type: StoryType = StoryType.STORY,
        priority: Priority = Priority.MEDIUM
    ) -> Dict:
        """
        Generate a Gherkin-formatted user story from natural language description

        Args:
            feature_description: Natural language description of the feature
            story_type: Type of story (epic, feature, story, task)
            priority: Priority level for the story

        Returns:
            Dictionary containing the generated story with metadata
        """
        try:
            logger.info(f"Generating story for: {feature_description[:50]}...")

            # Validate input
            if not feature_description or not feature_description.strip():
                raise ValueError("Feature description cannot be empty")

            # Clean and normalize the description
            normalized_description = self._normalize_description(
                feature_description)

            # Detect feature type and extract components
            feature_type = self._detect_feature_type(normalized_description)
            components = self._extract_story_components(
                normalized_description, feature_type)

            # Generate the Gherkin story
            gherkin_content = self._generate_gherkin_content(
                components, feature_type)

            # Calculate estimated effort (story points)
            estimated_effort = self._estimate_effort(
                normalized_description, feature_type)

            # Generate acceptance criteria
            acceptance_criteria = self._generate_acceptance_criteria(
                components, feature_type)

            # Create response object
            story_result = {
                'story_id': self._generate_story_id(),
                'feature_description': feature_description,
                'gherkin_content': gherkin_content,
                'acceptance_criteria': acceptance_criteria,
                'estimated_effort': estimated_effort,
                'story_type': story_type.value,
                'priority': priority.value,
                'feature_type': feature_type,
                'generated_at': datetime.utcnow().isoformat(),
                'components': components
            }

            logger.info(
                f"Successfully generated story with ID: {
                    story_result['story_id']}")
            return story_result

        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            raise

    def _normalize_description(self, description: str) -> str:
        """Clean and normalize the feature description"""
        # Remove extra whitespace and normalize case
        normalized = re.sub(r'\s+', ' ', description.strip().lower())

        # Remove common filler words for better analysis
        filler_words = [
            'the',
            'a',
            'an',
            'and',
            'or',
            'but',
            'in',
            'on',
            'at',
            'to',
            'for',
            'of',
            'with',
            'by']
        words = normalized.split()
        filtered_words = [
            word for word in words if word not in filler_words or len(words) <= 3]

        return ' '.join(filtered_words)

    def _detect_feature_type(self, description: str) -> str:
        """Detect the type of feature based on keywords in the description"""
        description_lower = description.lower()

        # Score each feature type based on keyword matches
        type_scores = {}
        for feature_type, config in self.templates.FEATURE_PATTERNS.items():
            score = sum(
                1 for keyword in config['keywords'] if keyword in description_lower)
            if score > 0:
                type_scores[feature_type] = score

        # Return the feature type with the highest score, or 'general' if no
        # match
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return 'general'

    def _extract_story_components(
            self,
            description: str,
            feature_type: str) -> Dict:
        """Extract key components from the feature description"""
        components = {
            'role': self._extract_user_role(description),
            'action': self._extract_action(description),
            'benefit': self._extract_benefit(description),
            'feature_name': self._extract_feature_name(
                description,
                feature_type)}

        return components

    def _extract_user_role(self, description: str) -> str:
        """Determine the appropriate user role based on the description"""
        description_lower = description.lower()

        for keyword, role in self.templates.USER_ROLES.items():
            if keyword in description_lower:
                return role

        return 'user'  # Default role

    def _extract_action(self, description: str) -> str:
        """Extract the main action from the description"""
        # Look for action verbs and construct a meaningful action phrase
        action_verbs = [
            'create',
            'add',
            'update',
            'edit',
            'delete',
            'remove',
            'view',
            'see',
            'manage',
            'search',
            'find',
            'upload',
            'download',
            'send',
            'receive',
            'login',
            'register',
            'authenticate',
            'access',
            'configure',
            'setup',
            'enable',
            'disable']

        description_words = description.split()

        # Find action verbs in the description
        found_actions = []
        for word in description_words:
            if word in action_verbs:
                found_actions.append(word)

        if found_actions:
            primary_action = found_actions[0]
            # Try to find the object of the action
            try:
                action_index = description_words.index(primary_action)
                if action_index < len(description_words) - 1:
                    object_part = ' '.join(
                        description_words[action_index + 1:action_index + 3])
                    return f"{primary_action} {object_part}".strip()
            except ValueError:
                pass

            return primary_action

        # If no action verb found, construct from the description
        return f"use {
            description.split()[0] if description.split() else 'the system'}"

    def _extract_benefit(self, description: str) -> str:
        """Extract or infer the benefit from the description"""
        # Common benefit patterns
        benefits = {
            'auth': 'securely access my account',
            'login': 'access the system securely',
            'search': 'quickly find the information I need',
            'upload': 'share and store my files',
            'manage': 'efficiently organize my data',
            'notification': 'stay informed about important updates',
            'api': 'integrate with external systems',
            'dashboard': 'have an overview of my information',
            'profile': 'maintain my personal information'
        }

        description_lower = description.lower()

        for keyword, benefit in benefits.items():
            if keyword in description_lower:
                return benefit

        # Default benefit based on common patterns
        if any(word in description_lower for word in ['create', 'add', 'new']):
            return 'easily add new information to the system'
        elif any(word in description_lower for word in ['update', 'edit', 'modify']):
            return 'keep my information current and accurate'
        elif any(word in description_lower for word in ['view', 'see', 'display']):
            return 'access the information I need'
        else:
            return 'accomplish my goals efficiently'

    def _extract_feature_name(
            self,
            description: str,
            feature_type: str) -> str:
        """Generate an appropriate feature name"""
        if feature_type in self.templates.FEATURE_PATTERNS:
            base_name = self.templates.FEATURE_PATTERNS[feature_type]['template']['feature']
        else:
            # Create a name from the description
            words = description.split()[:3]  # Take first 3 words
            base_name = ' '.join(word.capitalize() for word in words)

        return base_name

    def _generate_gherkin_content(
            self,
            components: Dict,
            feature_type: str) -> str:
        """Generate the formatted Gherkin content"""
        # Get template for the feature type
        if feature_type in self.templates.FEATURE_PATTERNS:
            template = self.templates.FEATURE_PATTERNS[feature_type]['template']
            scenarios = template['scenarios']
        else:
            # Use a generic template
            scenarios = [
                {
                    'name': 'Basic functionality',
                    'given': 'I am using the system',
                    'when': f'I {components["action"]}',
                    'then': f'I should be able to {components["benefit"]}'
                }
            ]

        # Build the Gherkin content
        gherkin_lines = [
            f"Feature: {components['feature_name']}",
            f"  As a {components['role']}",
            f"  I want to {components['action']}",
            f"  So that I can {components['benefit']}",
            ""
        ]

        # Add scenarios
        for scenario in scenarios:
            gherkin_lines.extend([
                f"  Scenario: {scenario['name']}",
                f"    Given {scenario['given']}",
                f"    When {scenario['when']}",
                f"    Then {scenario['then']}",
                ""
            ])

        return '\n'.join(gherkin_lines).rstrip()

    def _generate_acceptance_criteria(
            self,
            components: Dict,
            feature_type: str) -> List[str]:
        """Generate acceptance criteria for the story"""
        criteria = []

        # Base criteria from templates
        if feature_type in self.templates.FEATURE_PATTERNS:
            template = self.templates.FEATURE_PATTERNS[feature_type]['template']
            for scenario in template['scenarios']:
                criteria.append(
                    f"Given {
                        scenario['given']}, when {
                        scenario['when']}, then {
                        scenario['then']}")

        # Add common criteria
        criteria.extend([
            f"The {components['role']} should be able to {components['action']} successfully",
            "Appropriate error messages should be displayed for invalid inputs",
            "The feature should work across different browsers and devices"
        ])

        return criteria

    def _estimate_effort(self, description: str, feature_type: str) -> int:
        """Estimate story points based on complexity indicators"""
        # Base effort by feature type
        base_efforts = {
            'authentication': 8,
            'crud': 5,
            'api': 5,
            'search': 3,
            'file_management': 8,
            'notification': 3,
            'general': 3
        }

        base_effort = base_efforts.get(feature_type, 3)

        # Adjust based on complexity indicators
        complexity_keywords = {
            'integration': 2,
            'security': 2,
            'authentication': 2,
            'payment': 3,
            'real-time': 2,
            'dashboard': 2,
            'admin': 2,
            'reporting': 2,
            'analytics': 2,
            'ai': 3,
            'machine learning': 3,
            'complex': 2,
            'multiple': 1
        }

        description_lower = description.lower()
        complexity_bonus = 0

        for keyword, bonus in complexity_keywords.items():
            if keyword in description_lower:
                complexity_bonus += bonus

        # Calculate final effort (story points: 1, 2, 3, 5, 8, 13)
        total_effort = base_effort + complexity_bonus

        # Map to Fibonacci story points
        if total_effort <= 2:
            return 1
        elif total_effort <= 4:
            return 2
        elif total_effort <= 6:
            return 3
        elif total_effort <= 10:
            return 5
        elif total_effort <= 15:
            return 8
        else:
            return 13

    def _generate_story_id(self) -> str:
        """Generate a unique story ID"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"STORY_{timestamp}"

    def refine_story(
        self,
        story_id: str,
        refinement_feedback: str,
        original_story: Dict
    ) -> Dict:
        """
        Refine an existing story based on feedback

        Args:
            story_id: ID of the story to refine
            refinement_feedback: User feedback for refinement
            original_story: The original story dictionary

        Returns:
            Refined story dictionary
        """
        try:
            logger.info(
                f"Refining story {story_id} with feedback: "
                f"{refinement_feedback[:50]}..."
            )

            # Parse refinement feedback for additional requirements
            self._parse_refinement_feedback(refinement_feedback)

            # Update the original story with refinements
            refined_story = original_story.copy()

            # Re-generate with additional context
            combined_description = f"{
                original_story['feature_description']} {refinement_feedback}"
            refined_result = self.generate_gherkin_story(
                combined_description,
                StoryType(original_story['story_type']),
                Priority(original_story['priority'])
            )

            # Merge the results
            refined_story.update({
                'gherkin_content': refined_result['gherkin_content'],
                'acceptance_criteria': refined_result['acceptance_criteria'],
                'estimated_effort': refined_result['estimated_effort'],
                'refinement_feedback': refinement_feedback,
                'refined_at': datetime.utcnow().isoformat(),
                'version': refined_story.get('version', 1) + 1
            })

            logger.info(f"Successfully refined story {story_id}")
            return refined_story

        except Exception as e:
            logger.error(f"Error refining story {story_id}: {str(e)}")
            raise

    def _parse_refinement_feedback(self, feedback: str) -> List[str]:
        """Parse refinement feedback for additional requirements"""
        # Simple parsing - could be enhanced with NLP
        requirements = []

        feedback_lower = feedback.lower()

        # Look for explicit additions
        if 'add' in feedback_lower:
            requirements.append(feedback.strip())
        if 'include' in feedback_lower:
            requirements.append(feedback.strip())
        if 'also' in feedback_lower:
            requirements.append(feedback.strip())

        return requirements

    def validate_gherkin_syntax(
            self, gherkin_content: str) -> Tuple[bool, List[str]]:
        """
        Validate Gherkin syntax and return issues if any

        Args:
            gherkin_content: The Gherkin content to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        is_valid = True

        try:
            lines = gherkin_content.split('\n')

            # Check for required keywords
            has_feature = any(line.strip().startswith('Feature:')
                              for line in lines)
            if not has_feature:
                issues.append("Missing 'Feature:' declaration")
                is_valid = False

            has_scenario = any(line.strip().startswith('Scenario:')
                               for line in lines)
            if not has_scenario:
                issues.append("Missing 'Scenario:' declaration")
                is_valid = False

            # Check for Given-When-Then structure
            scenario_started = False
            has_given = False
            has_when = False
            has_then = False

            for line in lines:
                stripped = line.strip()
                if stripped.startswith('Scenario:'):
                    scenario_started = True
                    has_given = has_when = has_then = False
                elif scenario_started:
                    if stripped.startswith('Given'):
                        has_given = True
                    elif stripped.startswith('When'):
                        has_when = True
                    elif stripped.startswith('Then'):
                        has_then = True

            if scenario_started and not (has_given and has_when and has_then):
                missing_steps = []
                if not has_given:
                    missing_steps.append('Given')
                if not has_when:
                    missing_steps.append('When')
                if not has_then:
                    missing_steps.append('Then')
                issues.append(f"Missing step(s): {', '.join(missing_steps)}")
                is_valid = False

        except Exception as e:
            issues.append(f"Syntax validation error: {str(e)}")
            is_valid = False

        return is_valid, issues


# Utility functions for external use
def create_story_generator() -> StoryGenerator:
    """Factory function to create a new StoryGenerator instance"""
    return StoryGenerator()


def generate_story_from_description(description: str) -> Dict:
    """Convenience function to generate a story from a description"""
    generator = create_story_generator()
    return generator.generate_gherkin_story(description)


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    generator = StoryGenerator()

    # Test with different types of features
    test_descriptions = [
        "User authentication with social login",
        "File upload functionality for documents",
        "Search functionality for products",
        "Admin dashboard for managing users",
        "API endpoint for user data",
        "Real-time notifications for chat messages"
    ]

    print("=== Story Generator Demo ===\n")

    for description in test_descriptions:
        print(f"Input: {description}")
        try:
            result = generator.generate_gherkin_story(description)
            print(f"Generated Story (ID: {result['story_id']}):")
            print(result['gherkin_content'])
            print(
                f"Estimated Effort: {
                    result['estimated_effort']} story points")
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 50)
