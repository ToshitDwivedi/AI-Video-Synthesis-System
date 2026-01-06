"""
LLM client for script generation using Groq or Ollama.
"""

import os
import requests
from typing import Optional
import logging

logger = logging.getLogger('video_synthesis.llm')


class LLMClient:
    """Client for interacting with LLM (Groq or Ollama)."""
    
    def __init__(self, config: dict):
        """
        Initialize LLM client.
        
        Args:
            config: LLM configuration from config.yaml
        """
        self.config = config
        self.provider = config.get('provider', 'groq')
        
        if self.provider == 'groq':
            self.api_key = config['groq']['api_key']
            self.model = config['groq']['model']
            self.base_url = "https://api.groq.com/openai/v1/chat/completions"
            self.max_tokens = config['groq'].get('max_tokens', 4096)
            self.temperature = config['groq'].get('temperature', 0.7)
        elif self.provider == 'ollama':
            self.model = config['ollama']['model']
            self.base_url = config['ollama'].get('base_url', 'http://localhost:11434')
            self.temperature = config['ollama'].get('temperature', 0.7)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text from prompt.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Generated text
        """
        if self.provider == 'groq':
            return self._generate_groq(prompt, system_prompt)
        elif self.provider == 'ollama':
            return self._generate_ollama(prompt, system_prompt)
    
    def _generate_groq(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Groq API."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        logger.info(f"Generating with Groq model: {self.model}")
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            logger.info(f"Generated {len(generated_text)} characters")
            return generated_text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Groq API error: {e}")
            raise
    
    def _generate_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using local Ollama."""
        url = f"{self.base_url}/api/generate"
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }
        
        logger.info(f"Generating with Ollama model: {self.model}")
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['response']
            
            logger.info(f"Generated {len(generated_text)} characters")
            return generated_text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            logger.error("Make sure Ollama is running: ollama serve")
            raise
