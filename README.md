# ai-agent

## ReAct: Combine the reasoning and acting capabilities

*"Instead of asking GPT to simply do smart-autocomplete on your text, you prompt it to respond in a thought/act/observation loop"*

## Samples

- Sample 1

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

- Sample 2

```bash
❯ python main.py "Is Fan Zhendong win the Grand Slam of Table Tennis in 2024?"
======================================== Iterations 1 =============================================
>> Reasoning with the prompt/observation:
Thought: I should look up Fan Zhendong on Wikipedia to see if he has won any Grand Slams in Table Tennis.

Action: wikipedia: Fan Zhendong
PAUSE
>> Acting: wikipedia Fan Zhendong
>> Observation: <span class="searchmatch">Fan</span> <span class="searchmatch">Zhendong</span> (Chinese: 樊振东; pinyin: <span class="searchmatch">Fán</span> <span class="searchmatch">Zhèndōng</span>; born 22 January 1997) is a Chinese professional table tennis player. After joining the Chinese national
======================================== Iterations 2 =============================================
>> Reasoning with the prompt/observation:
Thought: I didn't find any information about Fan Zhendong winning the Grand Slam of Table Tennis in 2024 on Wikipedia. Let me try to find the latest news about Fan Zhendong.

Action: news: Fan Zhendong
PAUSE
>> Acting: news Fan Zhendong
>> Observation: Fan Zhendong triumphs over Truls Moregardh to extend China's table tennis dominance | Paris Olympics NBC SportsNovak Djokovic wins "Golden Slam" after beating Carlos Alcaraz for Olympic men's singles title CBS NewsDjokovic fights off Alcaraz to finally strike gold ReutersNovak Djokovic vs Carlos Alcaraz Tennis Men's Singles Final Live Streaming Olympics 2024 Live Teleca.. NDTV SportsParis 2024 table tennis: People's Republic of China's Fan Zhendong beats Sweden's Truls Möregårdh to win men's individual gold Olympics; Rezultati hrvatskih sportaša: → Filip Pravdica plasirao se u finale skoka u dalj, u kvalifikacijama je završio na petom mjestu → Matija Marinić nije uspio ući u četvrtfinale u disciplini kajak kros → Filip Jurišić je odradio sedmi i osmi plov te je trenutno na 19. mjestu → Aurel Benović završio je p...; Truls Möregårdh yllätti itsensäkin matkalla olympiahopealle.; Fan Zhendong’s table tennis gold cheers China and Taylor Swift fanatics The GuardianDjokovic beats Alcaraz to finally win his first Olympic gold Al Jazeera EnglishTable tennis: China's Chen beats teammate Sun again to defend women's singles title ReutersWhat time is Alcaraz vs Djokovik?: Schedule and where to watch the Tennis finals at the Olympics Marca.comChina’s Fan Zhendong wins table tennis singles gold, French teenager Felix Lebrun takes bronze The Straits Times; Le pongiste de 17 ans s’est offert le bronze, dimanche, en battant le Brésilien Hugo Calderano. La France ne s’était plus invitée sur un podium olympique individuel dans la discipline depuis 1992.
======================================== Iterations 3 =============================================
>> Reasoning with the prompt/observation:
Thought: I found some recent news about Fan Zhendong, but it's about him winning the men's individual gold in table tennis at the Paris 2024 Olympics. I still don't have a direct answer to whether he won the Grand Slam of Table Tennis in 2024. Let me try to find more information on Google.

Action: google: Fan Zhendong Grand Slam Table Tennis
PAUSE
>> Acting: google Fan Zhendong Grand Slam Table Tennis
>> Observation: Fan Zhendong is a Chinese professional table tennis player. After joining the Chinese national table tennis team in 2012 as the youngest member of the team, ...; China's paddler Fan Zhendong defeated Sweden's Truls Moregard 4-1 to win the gold medal in men's singles table tennis at the Paris Olympics ...; China's table tennis player Fan Zhendong in action during the men's singles final at the Paris Olympics on Sunday. [Photo by Wei Xiaohao ...; Fan Zhendong (CHN) Won Gold (MS) And Has Achieved Grand Slam! Discussion.
======================================== Iterations 4 =============================================
>> Reasoning with the prompt/observation:
Thought: Ah-ha! I finally found the answer. According to the observation, Fan Zhendong has achieved a Grand Slam, which is a great accomplishment in table tennis. Although it doesn't specifically mention the year 2024, it seems that he has achieved the Grand Slam recently, considering the other recent news articles about his win at the Paris Olympics.

Answer: Yes, Fan Zhendong has won the Grand Slam of Table Tennis.
```

## References

- The Paper: [ReAct: Synergizing Reasoning and Acting in Language Models](https://react-lm.github.io/)

- Materials: 
  - [A simple Python implementation of the ReAct pattern for LLMs](https://til.simonwillison.net/llms/python-react-pattern)
  - [Interconnected The surprising ease and effectiveness of AI in a loop](https://interconnected.org/home/2023/03/16/singularity)

- Code
  - [A simple Python wrapper for the ChatGPT API](https://til.simonwillison.net/gpt3/chatgpt-api)
  - https://github.com/alejandro-ao/agents-no-framework