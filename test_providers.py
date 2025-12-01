"""
Test script for LLM Provider Processor.

Tests the centralized provider configuration system.
"""

from llm_provider import LLMProviderProcessor

print("="*70)
print("Testing LLM Provider Processor")
print("="*70)

# Test 1: Show available providers
print("\n1. Available Providers:")
providers = LLMProviderProcessor.get_available_providers()
print(f"   {', '.join(providers)}")

# Test 2: Get default models
print("\n2. Default Models:")
for provider in providers:
    model = LLMProviderProcessor.get_default_model(provider)
    print(f"   {provider}: {model}")

# Test 3: Test configuration for each provider
print("\n3. Provider Configuration Tests:")
for provider in providers:
    try:
        config = LLMProviderProcessor.get_config(provider=provider)
        print(f"\n   ✓ {provider.upper()} Configuration:")
        print(f"     Model: {config.model_name}")
        print(f"     Base URL: {config.base_url or 'Default (OpenAI)'}")
        print(f"     API Key: {'*' * 10}{config.api_key[-4:] if len(config.api_key) > 4 else '****'}")
        print(f"     Temperature: {config.temperature}")
    except ValueError as e:
        print(f"\n   ✗ {provider.upper()}: {e}")

# Test 4: Test invalid provider
print("\n4. Invalid Provider Test:")
try:
    config = LLMProviderProcessor.get_config(provider="invalid")
    print("   ✗ Should have raised ValueError")
except ValueError as e:
    print(f"   ✓ Correctly rejected: {e}")

# Test 5: Test custom model
print("\n5. Custom Model Test:")
try:
    config = LLMProviderProcessor.get_config(
        provider="openrouter",
        model_name="anthropic/claude-3-sonnet"
    )
    print(f"   ✓ Custom model set: {config.model_name}")
except ValueError as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*70)
print("Test Complete!")
print("="*70)
