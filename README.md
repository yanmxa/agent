# ai-agent

## ReAct: Combine the reasoning and acting capabilities

*"Instead of asking GPT to simply do smart-autocomplete on your text, you prompt it to respond in a thought/act/observation loop"*

## Sample

```python
❯ python main.py "what's the Capital of France"
======================================== Iterations 1 =============================================
>> Reasoning with the prompt/observation:
Thought: I should look up France on Wikipedia

Action: wikipedia: France

PAUSE
>> Acting: wikipedia France
>> Observation: <span class="searchmatch">France</span>, officially the <span class="searchmatch">French</span> Republic, is a country located primarily in Western Europe. It also includes overseas regions and territories in the Americas
======================================== Iterations 2 =============================================
>> Reasoning with the prompt/observation:
Thought: That's not what I was looking for. I want to know the capital of France.

Action: wikipedia: France capital

PAUSE
>> Acting: wikipedia France capital
>> Observation: <span class="searchmatch">Capital</span> punishment in <span class="searchmatch">France</span> (<span class="searchmatch">French</span>: peine de mort en <span class="searchmatch">France</span>) is banned by Article 66-1 of the Constitution of the <span class="searchmatch">French</span> Republic, voted as a constitutional
======================================== Iterations 3 =============================================
>> Reasoning with the prompt/observation:
Thought: Still not the capital! It seems I'm getting sidetracked. I'll try something different.

Action: wikipedia: France capital city

PAUSE
>> Acting: wikipedia France capital city
>> Observation: A <span class="searchmatch">capital</span> <span class="searchmatch">city</span> or just <span class="searchmatch">capital</span> is the municipality holding primary status in a country, state, province, department, or other subnational division, usually
======================================== Iterations 4 =============================================
>> Reasoning with the prompt/observation:
Thought: Ah-ha! I think I see the pattern now. Wikipedia isn't providing the direct answer I want. Let me try searching on Google instead.

Action: google: capital of France

PAUSE
>> Acting: google capital of France
>> Observation: The City of Paris is the centre of the Île-de-France region, or Paris Region, with an official estimated population of 12,271,794 inhabitants in January 2023, ...; Paris is the capital and most populous city of France. Situated on the Seine River, in the north of the country, it is in the centre of the Île-de-France ...
======================================== Iterations 5 =============================================
>> Reasoning with the prompt/observation:
Thought: Ah, finally! I think I can confidently say that...

Answer: The capital of France is Paris.
You get the point
```

## References

- The Paper: [ReAct: Synergizing Reasoning and Acting in Language Models](https://react-lm.github.io/)

- Materials: 
  - [A simple Python implementation of the ReAct pattern for LLMs](https://til.simonwillison.net/llms/python-react-pattern)
  - [Interconnected The surprising ease and effectiveness of AI in a loop](https://interconnected.org/home/2023/03/16/singularity)

- Code
  - [A simple Python wrapper for the ChatGPT API](https://til.simonwillison.net/gpt3/chatgpt-api)
  - https://github.com/alejandro-ao/agents-no-framework