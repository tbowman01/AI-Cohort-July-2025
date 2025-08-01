"""
Test script for story generation functionality

This script tests the core story generation services to ensure
they work correctly for the demo.
"""

from schemas.story_schemas import StoryGenerationRequest, StoryResponse
from services.ai_client import AIClient, create_ai_client
from services.story_generator import StoryGenerator, StoryType, Priority
import asyncio
import json
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def test_story_generator():
    """Test the template-based story generator"""
    print("=== Testing Story Generator ===")

    generator = StoryGenerator()

    # Test different feature types
    test_cases = [
        {
            "description": "User authentication with social login",
            "expected_type": "authentication",
            "story_type": StoryType.FEATURE,
            "priority": Priority.HIGH
        },
        {
            "description": "File upload functionality for documents",
            "expected_type": "file_management",
            "story_type": StoryType.STORY,
            "priority": Priority.MEDIUM
        },
        {
            "description": "Search functionality with filters and sorting",
            "expected_type": "search",
            "story_type": StoryType.STORY,
            "priority": Priority.MEDIUM
        },
        {
            "description": "Admin dashboard for managing users and roles",
            "expected_type": "crud",
            "story_type": StoryType.EPIC,
            "priority": Priority.HIGH
        },
        {
            "description": "Real-time notifications for chat messages",
            "expected_type": "notification",
            "story_type": StoryType.STORY,
            "priority": Priority.LOW
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['description'][:50]}... ---")

        try:
            # Generate story
            result = generator.generate_gherkin_story(
                test_case['description'],
                test_case['story_type'],
                test_case['priority']
            )

            # Validate results
            assert result['story_id'], "Story ID should be generated"
            assert result['gherkin_content'], "Gherkin content should be generated"
            assert result['acceptance_criteria'], "Acceptance criteria should be generated"
            assert result['estimated_effort'] >= 1, "Effort should be at least 1"
            assert result['feature_type'], "Feature type should be detected"

            # Validate Gherkin syntax
            is_valid, issues = generator.validate_gherkin_syntax(
                result['gherkin_content'])

            print(f"✅ Story ID: {result['story_id']}")
            print(
                f"✅ Feature Type: {result['feature_type']} (expected: {test_case['expected_type']})")
            print(
                f"✅ Estimated Effort: {result['estimated_effort']} story points")
            print(f"✅ Valid Gherkin: {is_valid}")
            print(
                f"✅ Acceptance Criteria: {len(result['acceptance_criteria'])} items")

            if not is_valid:
                print(f"❌ Gherkin Issues: {issues}")

            # Display generated story
            print("\nGenerated Gherkin Story:")
            print("-" * 40)
            print(result['gherkin_content'])
            print("-" * 40)

            results.append({
                'test_case': i,
                'description': test_case['description'],
                'success': True,
                'story_id': result['story_id'],
                'feature_type': result['feature_type'],
                'valid_gherkin': is_valid,
                'effort': result['estimated_effort']
            })

        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            results.append({
                'test_case': i,
                'description': test_case['description'],
                'success': False,
                'error': str(e)
            })

    # Summary
    successful_tests = sum(1 for r in results if r['success'])
    print(f"\n=== Story Generator Test Summary ===")
    print(f"Passed: {successful_tests}/{len(test_cases)}")
    print(f"Success Rate: {successful_tests / len(test_cases) * 100:.1f}%")

    return results


async def test_ai_client():
    """Test the AI client with fallback to template generation"""
    print("\n=== Testing AI Client ===")

    client = create_ai_client()

    # Test provider status
    status = client.get_provider_status()
    print(f"AI Provider Status: {json.dumps(status, indent=2)}")

    # Test story generation
    test_description = "API endpoint for user profile management with CRUD operations"

    try:
        print(f"\nGenerating story with AI client for: {test_description}")

        result = await client.generate_story_with_ai(test_description)

        # Validate results
        assert result['story_id'], "Story ID should be generated"
        assert result['gherkin_content'], "Gherkin content should be generated"
        assert 'ai_provider' in result, "AI provider info should be included"

        print(f"✅ Story generated successfully")
        print(f"✅ AI Provider: {result.get('ai_provider', 'unknown')}")
        print(f"✅ Template Based: {result.get('template_based', False)}")
        print(f"✅ Confidence Score: {result.get('confidence_score', 'N/A')}")

        # Test story quality analysis
        quality = await client.analyze_story_quality(result['gherkin_content'])
        print(f"✅ Quality Score: {quality['quality_score']:.2f}")
        print(f"✅ Valid Gherkin: {quality['is_valid_gherkin']}")

        # Test suggestions
        suggestions = await client.get_story_suggestions(test_description)
        print(f"✅ Suggestions: {len(suggestions)} items")

        # Test refinement
        refinement_feedback = "Add authentication and authorization requirements"
        refined = await client.refine_story_with_ai(
            result['story_id'],
            result,
            refinement_feedback
        )

        print(f"✅ Story refined successfully")
        print(f"✅ Refined Version: {refined.get('version', 1)}")

        return True

    except Exception as e:
        print(f"❌ AI Client test failed: {str(e)}")
        return False


async def test_schema_validation():
    """Test Pydantic schema validation"""
    print("\n=== Testing Schema Validation ===")

    try:
        # Test valid request
        valid_request = StoryGenerationRequest(
            feature_description="User authentication with multi-factor authentication",
            story_type="feature",
            priority="high",
            use_ai=True)
        print("✅ Valid request schema passes validation")

        # Test invalid requests
        try:
            invalid_request = StoryGenerationRequest(
                feature_description="",  # Empty description should fail
                story_type="feature",
                priority="high"
            )
            print("❌ Empty description should have failed validation")
            return False
        except Exception:
            print("✅ Empty description correctly rejected")

        try:
            invalid_request = StoryGenerationRequest(
                feature_description="Short",  # Too short should fail
                story_type="feature",
                priority="high"
            )
            print("❌ Short description should have failed validation")
            return False
        except Exception:
            print("✅ Short description correctly rejected")

        # Test response schema
        sample_story_data = {
            'story_id': 'TEST_STORY_001',
            'feature_description': 'Test feature',
            'gherkin_content': 'Feature: Test\n  Scenario: Test',
            'acceptance_criteria': ['Test criterion'],
            'estimated_effort': 5,
            'story_type': 'story',
            'priority': 'medium',
            'generated_at': datetime.utcnow().isoformat()
        }

        response = StoryResponse(**sample_story_data)
        print("✅ Response schema validation passes")

        return True

    except Exception as e:
        print(f"❌ Schema validation test failed: {str(e)}")
        return False


async def test_integration():
    """Test integration between components"""
    print("\n=== Testing Component Integration ===")

    try:
        # Initialize components
        generator = StoryGenerator()
        ai_client = create_ai_client()

        # Test end-to-end workflow
        feature_description = "Real-time collaborative document editing with version control"

        # Generate story
        story_result = generator.generate_gherkin_story(feature_description)
        print(f"✅ Story generated: {story_result['story_id']}")

        # Analyze quality
        quality = await ai_client.analyze_story_quality(story_result['gherkin_content'])
        print(f"✅ Quality analyzed: {quality['quality_score']:.2f}")

        # Get suggestions
        suggestions = await ai_client.get_story_suggestions(feature_description)
        print(f"✅ Suggestions generated: {len(suggestions)} items")

        # Refine story
        refinement_feedback = "Add real-time conflict resolution and user presence indicators"
        refined_story = generator.refine_story(
            story_result['story_id'],
            refinement_feedback,
            story_result
        )
        print(f"✅ Story refined: version {refined_story.get('version', 1)}")

        # Validate final result
        is_valid, issues = generator.validate_gherkin_syntax(
            refined_story['gherkin_content'])
        print(f"✅ Final validation: {'Valid' if is_valid else 'Invalid'}")

        if issues:
            print(f"⚠️ Validation issues: {issues}")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False


async def demo_story_generation():
    """Demo the story generation functionality with example outputs"""
    print("\n" + "=" * 60)
    print("AUTODEVHUB STORY GENERATION DEMO")
    print("=" * 60)

    generator = StoryGenerator()

    demo_features = [
        "User registration with email verification and profile setup",
        "Admin dashboard for monitoring system performance and user activity",
        "Mobile app push notifications for order status updates",
        "API rate limiting and authentication for third-party integrations",
        "Document collaboration with real-time editing and comments"
    ]

    for i, feature in enumerate(demo_features, 1):
        print(f"\n🎯 Demo {i}: {feature}")
        print("-" * 60)

        try:
            result = generator.generate_gherkin_story(
                feature,
                StoryType.FEATURE,
                Priority.MEDIUM
            )

            print(f"📋 Story ID: {result['story_id']}")
            print(f"🎯 Feature Type: {result['feature_type']}")
            print(f"📊 Effort: {result['estimated_effort']} story points")
            print(f"✅ Criteria: {len(result['acceptance_criteria'])} items")

            print("\n📝 Generated Gherkin Story:")
            print(result['gherkin_content'])

            print(f"\n📋 Acceptance Criteria:")
            for j, criterion in enumerate(result['acceptance_criteria'], 1):
                print(f"  {j}. {criterion}")

        except Exception as e:
            print(f"❌ Demo failed: {str(e)}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETED")
    print("=" * 60)


async def main():
    """Run all tests"""
    print("🚀 Starting AutoDevHub Story Generation Tests")
    print("=" * 60)

    # Run individual tests
    test_results = []

    # Test story generator
    generator_results = await test_story_generator()
    test_results.append(('Story Generator',
                         len([r for r in generator_results if r['success']]),
                         len(generator_results)))

    # Test AI client
    ai_result = await test_ai_client()
    test_results.append(('AI Client', 1 if ai_result else 0, 1))

    # Test schema validation
    schema_result = await test_schema_validation()
    test_results.append(('Schema Validation', 1 if schema_result else 0, 1))

    # Test integration
    integration_result = await test_integration()
    test_results.append(('Integration', 1 if integration_result else 0, 1))

    # Overall summary
    total_passed = sum(passed for _, passed, _ in test_results)
    total_tests = sum(total for _, _, total in test_results)

    print(f"\n" + "=" * 60)
    print("FINAL TEST SUMMARY")
    print("=" * 60)

    for test_name, passed, total in test_results:
        success_rate = (passed / total * 100) if total > 0 else 0
        status = "✅ PASS" if passed == total else "❌ FAIL"
        print(f"{test_name:<20}: {passed}/{total} ({success_rate:.1f}%) {status}")

    overall_success_rate = (
        total_passed /
        total_tests *
        100) if total_tests > 0 else 0
    overall_status = "✅ ALL TESTS PASSED" if total_passed == total_tests else "❌ SOME TESTS FAILED"

    print("-" * 60)
    print(f"{'OVERALL':<20}: {total_passed}/{total_tests} ({overall_success_rate:.1f}%) {overall_status}")
    print("=" * 60)

    # Run demo if tests are mostly successful
    if overall_success_rate >= 80:
        await demo_story_generation()

    return overall_success_rate >= 80


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
