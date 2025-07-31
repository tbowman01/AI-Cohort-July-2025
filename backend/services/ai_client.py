"""
AI Client Service for AutoDevHub

This service provides AI integration capabilities for enhanced story generation,
with fallback to template-based generation for reliable demo functionality.
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """Supported AI providers"""
    CLAUDE = "claude"
    OPENAI = "openai"
    LOCAL = "local"
    TEMPLATE = "template"  # Fallback to template-based generation


class AIClientConfig:
    """Configuration for AI clients"""
    
    def __init__(self):
        self.claude_api_key = os.getenv("CLAUDE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.max_retries = 3
        self.timeout_seconds = 30
        self.fallback_to_template = True
        
        # AI prompt templates for story generation
        self.story_generation_prompt = """
        You are an expert Agile coach and product manager. Generate a comprehensive user story in Gherkin format based on the following feature description:
        
        Feature Description: {feature_description}
        
        Please provide:
        1. A well-formed user story with "As a [role], I want [functionality], So that [benefit]"
        2. Acceptance criteria in Given-When-Then format
        3. Edge cases and error scenarios
        4. Estimated story points (1, 2, 3, 5, 8, 13)
        5. Dependencies and assumptions
        
        Format the response in valid Gherkin syntax with proper indentation and keywords.
        Return the response as a JSON object with the following structure:
        {
            "gherkin_content": "Feature: ...",
            "acceptance_criteria": ["criterion1", "criterion2"],
            "estimated_effort": 5,
            "dependencies": ["dep1", "dep2"],
            "assumptions": ["assumption1", "assumption2"]
        }
        """
        
        self.story_refinement_prompt = """
        You are an expert Agile coach refining a user story based on feedback.
        
        Original Story:
        {original_story}
        
        Refinement Feedback:
        {feedback}
        
        Please refine the story incorporating the feedback while maintaining proper Gherkin format.
        Return the response as a JSON object with the same structure as the original.
        """


class AIClient:
    """AI client for story generation and enhancement"""
    
    def __init__(self, config: Optional[AIClientConfig] = None):
        """Initialize AI client with configuration"""
        self.config = config or AIClientConfig()
        self.available_providers = self._detect_available_providers()
        self.current_provider = self._select_provider()
        
        logger.info(f"AIClient initialized with provider: {self.current_provider.value}")
        logger.info(f"Available providers: {[p.value for p in self.available_providers]}")
    
    def _detect_available_providers(self) -> List[AIProvider]:
        """Detect which AI providers are available based on configuration"""
        available = [AIProvider.TEMPLATE]  # Always available as fallback
        
        if self.config.claude_api_key:
            available.append(AIProvider.CLAUDE)
            logger.info("Claude API key detected")
        
        if self.config.openai_api_key:
            available.append(AIProvider.OPENAI)
            logger.info("OpenAI API key detected")
        
        return available
    
    def _select_provider(self) -> AIProvider:
        """Select the best available AI provider"""
        # Priority order: Claude > OpenAI > Template
        if AIProvider.CLAUDE in self.available_providers:
            return AIProvider.CLAUDE
        elif AIProvider.OPENAI in self.available_providers:
            return AIProvider.OPENAI
        else:
            return AIProvider.TEMPLATE
    
    async def generate_story_with_ai(
        self, 
        feature_description: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate a user story using AI with fallback to template-based generation
        
        Args:
            feature_description: Natural language description of the feature
            context: Additional context for story generation
            
        Returns:
            Dictionary containing AI-generated story content
        """
        try:
            logger.info(f"Generating story with AI using {self.current_provider.value}")
            
            if self.current_provider == AIProvider.CLAUDE:
                return await self._generate_with_claude(feature_description, context)
            elif self.current_provider == AIProvider.OPENAI:
                return await self._generate_with_openai(feature_description, context)
            else:
                return await self._generate_with_template(feature_description, context)
                
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            
            if self.config.fallback_to_template:
                logger.info("Falling back to template-based generation")
                return await self._generate_with_template(feature_description, context)
            else:
                raise
    
    async def _generate_with_claude(
        self, 
        feature_description: str, 
        context: Optional[Dict] = None
    ) -> Dict:
        """Generate story using Claude AI (placeholder implementation)"""
        logger.info("Claude AI integration not yet implemented - using template fallback")
        
        # TODO: Implement actual Claude API integration
        # For now, fall back to template-based generation
        return await self._generate_with_template(feature_description, context)
    
    async def _generate_with_openai(
        self, 
        feature_description: str, 
        context: Optional[Dict] = None
    ) -> Dict:
        """Generate story using OpenAI GPT (placeholder implementation)"""
        logger.info("OpenAI integration not yet implemented - using template fallback")
        
        # TODO: Implement actual OpenAI API integration
        # For now, fall back to template-based generation
        return await self._generate_with_template(feature_description, context)
    
    async def _generate_with_template(
        self, 
        feature_description: str, 
        context: Optional[Dict] = None
    ) -> Dict:
        """Generate story using template-based approach (reliable fallback)"""
        from .story_generator import StoryGenerator
        
        logger.info("Using template-based story generation")
        
        # Use the template-based story generator
        generator = StoryGenerator()
        result = generator.generate_gherkin_story(feature_description)
        
        # Add AI-specific metadata
        result.update({
            'ai_provider': 'template',
            'ai_generated': False,
            'template_based': True,
            'confidence_score': 0.85  # High confidence in template-based generation
        })
        
        return result
    
    async def refine_story_with_ai(
        self,
        story_id: str,
        original_story: Dict,
        refinement_feedback: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Refine an existing story using AI with feedback
        
        Args:
            story_id: ID of the story to refine
            original_story: The original story dictionary
            refinement_feedback: User feedback for refinement
            context: Additional context for refinement
            
        Returns:
            Dictionary containing refined story content
        """
        try:
            logger.info(f"Refining story {story_id} with AI using {self.current_provider.value}")
            
            if self.current_provider == AIProvider.CLAUDE:
                return await self._refine_with_claude(story_id, original_story, refinement_feedback, context)
            elif self.current_provider == AIProvider.OPENAI:
                return await self._refine_with_openai(story_id, original_story, refinement_feedback, context)
            else:
                return await self._refine_with_template(story_id, original_story, refinement_feedback, context)
                
        except Exception as e:
            logger.error(f"AI refinement failed: {str(e)}")
            
            if self.config.fallback_to_template:
                logger.info("Falling back to template-based refinement")
                return await self._refine_with_template(story_id, original_story, refinement_feedback, context)
            else:
                raise
    
    async def _refine_with_claude(
        self,
        story_id: str,
        original_story: Dict,
        refinement_feedback: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Refine story using Claude AI (placeholder implementation)"""
        logger.info("Claude AI refinement not yet implemented - using template fallback")
        
        # TODO: Implement actual Claude API refinement
        return await self._refine_with_template(story_id, original_story, refinement_feedback, context)
    
    async def _refine_with_openai(
        self,
        story_id: str,
        original_story: Dict,
        refinement_feedback: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Refine story using OpenAI GPT (placeholder implementation)"""
        logger.info("OpenAI refinement not yet implemented - using template fallback")
        
        # TODO: Implement actual OpenAI API refinement
        return await self._refine_with_template(story_id, original_story, refinement_feedback, context)
    
    async def _refine_with_template(
        self,
        story_id: str,
        original_story: Dict,
        refinement_feedback: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Refine story using template-based approach"""
        from .story_generator import StoryGenerator
        
        logger.info("Using template-based story refinement")
        
        # Use the template-based story generator for refinement
        generator = StoryGenerator()
        result = generator.refine_story(story_id, refinement_feedback, original_story)
        
        # Add AI-specific metadata
        result.update({
            'ai_provider': 'template',
            'ai_refined': False,
            'template_refined': True,
            'refinement_confidence': 0.80
        })
        
        return result
    
    async def analyze_story_quality(self, gherkin_content: str) -> Dict:
        """
        Analyze the quality of a generated story
        
        Args:
            gherkin_content: The Gherkin content to analyze
            
        Returns:
            Dictionary containing quality analysis
        """
        from .story_generator import StoryGenerator
        
        generator = StoryGenerator()
        is_valid, issues = generator.validate_gherkin_syntax(gherkin_content)
        
        # Calculate quality metrics
        lines = gherkin_content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        quality_score = 1.0
        
        # Deduct points for issues
        if not is_valid:
            quality_score -= len(issues) * 0.1
        
        # Bonus points for comprehensive scenarios
        scenario_count = sum(1 for line in lines if line.strip().startswith('Scenario:'))
        if scenario_count >= 2:
            quality_score += 0.1
        
        # Ensure score is between 0 and 1
        quality_score = max(0.0, min(1.0, quality_score))
        
        return {
            'quality_score': quality_score,
            'is_valid_gherkin': is_valid,
            'syntax_issues': issues,
            'scenario_count': scenario_count,
            'line_count': len(non_empty_lines),
            'completeness': {
                'has_feature': any('Feature:' in line for line in lines),
                'has_user_story': any('As a' in line for line in lines),
                'has_scenarios': scenario_count > 0,
                'has_given_when_then': all(
                    any(keyword in gherkin_content for keyword in [f'{step}'])
                    for step in ['Given', 'When', 'Then']
                )
            },
            'analyzed_at': datetime.utcnow().isoformat()
        }
    
    async def get_story_suggestions(self, feature_description: str) -> List[str]:
        """
        Get suggestions for improving a feature description
        
        Args:
            feature_description: The feature description to analyze
            
        Returns:
            List of suggestions for improvement
        """
        suggestions = []
        
        description_lower = feature_description.lower()
        
        # Check for common issues and provide suggestions
        if len(feature_description.split()) < 5:
            suggestions.append("Consider providing more detail about the feature requirements")
        
        if not any(word in description_lower for word in ['user', 'admin', 'customer', 'developer']):
            suggestions.append("Specify who will be using this feature (user role)")
        
        if not any(word in description_lower for word in ['should', 'must', 'need', 'want', 'require']):
            suggestions.append("Include what the feature should accomplish or enable")
        
        if 'authentication' in description_lower and 'security' not in description_lower:
            suggestions.append("Consider mentioning security requirements for authentication features")
        
        if any(word in description_lower for word in ['file', 'upload', 'download']) and 'format' not in description_lower:
            suggestions.append("Specify supported file formats and size limitations")
        
        if any(word in description_lower for word in ['search', 'find']) and 'result' not in description_lower:
            suggestions.append("Describe how search results should be displayed or filtered")
        
        # Add general suggestions if none specific found
        if not suggestions:
            suggestions.extend([
                "Consider adding acceptance criteria or success conditions",
                "Think about error scenarios and edge cases",
                "Specify any integration requirements with existing systems"
            ])
        
        return suggestions
    
    def get_provider_status(self) -> Dict:
        """Get the current status of AI providers"""
        return {
            'current_provider': self.current_provider.value,
            'available_providers': [p.value for p in self.available_providers],
            'claude_configured': AIProvider.CLAUDE in self.available_providers,
            'openai_configured': AIProvider.OPENAI in self.available_providers,
            'fallback_enabled': self.config.fallback_to_template,
            'status': 'operational'
        }


# Factory functions
def create_ai_client(config: Optional[AIClientConfig] = None) -> AIClient:
    """Factory function to create a new AIClient instance"""
    return AIClient(config)


async def generate_ai_enhanced_story(feature_description: str) -> Dict:
    """Convenience function to generate an AI-enhanced story"""
    client = create_ai_client()
    return await client.generate_story_with_ai(feature_description)


# Example usage and testing
if __name__ == "__main__":
    async def main():
        print("=== AI Client Demo ===\n")
        
        client = create_ai_client()
        
        # Show provider status
        status = client.get_provider_status()
        print("AI Provider Status:")
        print(json.dumps(status, indent=2))
        print()
        
        # Test story generation
        test_description = "User authentication with social login and two-factor authentication"
        
        print(f"Generating story for: {test_description}")
        
        try:
            result = await client.generate_story_with_ai(test_description)
            print("\nGenerated Story:")
            print(result['gherkin_content'])
            
            # Analyze quality
            quality = await client.analyze_story_quality(result['gherkin_content'])
            print(f"\nQuality Score: {quality['quality_score']:.2f}")
            print(f"Valid Gherkin: {quality['is_valid_gherkin']}")
            
            # Get suggestions
            suggestions = await client.get_story_suggestions(test_description)
            print("\nSuggestions:")
            for suggestion in suggestions:
                print(f"- {suggestion}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Run the async example
    asyncio.run(main())