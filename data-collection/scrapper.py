import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

csv_directory = os.path.join(os.path.dirname(__file__), 'CSV') 
progress_directory = os.path.join(os.path.dirname(__file__), 'progress')

# Amazon EC2 Auto Scaling FAQs(https://web.archive.org/web/20240727083813/https://aws.amazon.com/ec2/autoscaling/faqs/)
class AutoScalingFAQs():
    
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727090427/https://aws.amazon.com/ec2/autoscaling/faqs/'
        response = requests.get(URL,timeout=5)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/auto_scalling.csv'
        self.progress_file = f'{progress_directory}/auto_scalling.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                expandable_sections = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(expandable_sections):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text, 
                                'answer': content_div.get_text(), 
                                'category':'Auto Scalling',
                                'sub_category':category_h2.text})
                    
                    progress_file.write(f'Scraped {i+1}/{len(expandable_sections)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped AutoScalingFAQs\n')            

# Amazon Elastic Container Registry FAQs (https://web.archive.org/web/20240727090456/https://aws.amazon.com/ecr/faqs/)
class ElasticContainerRegistryFAQs():
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727090456/https://aws.amazon.com/ecr/faqs/'
        response = requests.get(URL,timeout=5)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/elastic_container_registry.csv'
        self.progress_file = f'{progress_directory}/elastic_container_registry.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the categories
        categories = self.soup.find_all('div', class_='lb-grid')
        categories = [div for div in categories if div.get('class') == ['lb-grid']]
        
        output = []
        
        with open(self.progress_file, 'w') as progress_file:
            # progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(categories)}\n\n')
            for category in categories:
                
                div = category.find('div', class_='lb-col lb-tiny-24 lb-mid-24')
                category_h2 = div.find('h2', class_='lb-txt-bold lb-txt-24 lb-h2 lb-title')
                content = div.find('div', class_='lb-txt-16 lb-rtxt')

                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                for a_tag in content.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))

                faqs = content.get_text().strip().split('Q:')[1:]
                for i, faq in enumerate(faqs):
                    que, ans = faq.split('?')[:2]
                    que = f'Q: {que.strip()}?'

                    output.append({
                    'question': que, 
                    'answer': ans.strip(),
                    'category':'Elastic Container Registry', 
                    'sub_category':category_h2.text.strip()})
                
                    progress_file.write(f'Scraped {i+1}/{len(faqs)} FAQs\n')
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')

            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
        print('[DONE] Scraped ElasticContainerRegistryFAQs\n')

# Amazon Elastic Container Service(ECS) FAQs(https://web.archive.org/web/20240727055400/https://aws.amazon.com/ec2/faqs/)
class ElasticContainerServiceFAQs():
    
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727083813/https://aws.amazon.com/ecs/faqs/'
        response = requests.get(URL, timeout=5)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/ecs.csv'
        self.progress_file = f'{progress_directory}/ecs.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                expandable_sections = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(expandable_sections):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text.strip(), 
                                'answer': content_div.get_text().strip(),
                                'category':'Elastic Container Service', 
                                'sub_category':category_h2.text.strip()})
                    
                    progress_file.write(f'Scraped {i+1}/{len(expandable_sections)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=True)
            print('[DONE] Scraped ElasticContainerServiceFAQs\n')

# Amazon EC2 FAQs (https://web.archive.org/web/20240727055400/https://aws.amazon.com/ec2/faqs/)
class EC2FAQs():
    
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727055400/https://aws.amazon.com/ec2/faqs/'
        response = requests.get(URL, timeout=5)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/ec2.csv'
        self.progress_file = f'{progress_directory}/ec2.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                try:
                    new_content = f"[{tag.text}]({tag['href']})"
                    return new_content
                except KeyError:
                    pass
            return str(tag)
        
        # Extracting the categories
        categories = self.soup.find_all('div', class_='lb-grid')
        categories = [div for div in categories if div.get('class') == ['lb-grid']]
        
        output = []
        
        count = 1
        with open(self.progress_file, 'w') as progress_file:
            for category in categories:
                
                div = category.find('div', class_='lb-col lb-tiny-24 lb-mid-24')
                
                title_classes = {'lb-txt-bold', 'lb-txt-20', 'lb-title'}
                tags = div.find_all()
                title_tag = [tag for tag in tags if title_classes.issubset(set(tag.get('class', [])))]
                title_tag = title_tag[0].text.strip() if len(title_tag) > 0 else ''
                
                contents = div.find_all('div', class_='lb-txt-16 lb-rtxt')
                progress_file.write(f'{"="*5} {title_tag} {"="*5}\n')
                
                faqs = ''
                for content in contents:
                    for a_tag in content.find_all('a'):
                            a_tag.replace_with(replace_a_tag(a_tag))
                    faqs += content.get_text().strip()

                faqs = faqs.split('Q:')[1:]
                for i, faq in enumerate(faqs):
                    que, ans = faq.split('?')[:2]
                    que = f'Q: {que.strip()}?'

                    output.append({
                    'question': que, 
                    'answer': ans.strip(), 
                    'category':'EC 2',
                    'sub_category':title_tag})
                
                    progress_file.write(f'Scraped {i+1}/{len(faqs)} FAQs\n')
                    count += 1
                progress_file.write(f'{"="*5}{"="*(len(title_tag)+2)}{"="*5}\n\n')
            
            progress_file.write(f'Total FAQs: {count}\n')
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped EC2FAQs\n')

# Amazon Elastic Kubernetes Service(EKS) FAQs (https://web.archive.org/web/20240727090537/https://aws.amazon.com/eks/faqs/)
class ElasticKubernetesFAQs():
    
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727090537/https://aws.amazon.com/eks/faqs/'
        response = requests.get(URL,timeout=5)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/elastic_kubernetes_service.csv'
        self.progress_file = f'{progress_directory}/elastic_kubernetes_service.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the categories
        categories = self.soup.find_all('div', class_='lb-grid')
        categories = [div for div in categories if div.get('class') == ['lb-grid']]
        
        output = []
        
        with open(self.progress_file, 'w') as progress_file:
            # progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(categories)}\n\n')
            for category in categories:
                
                div = category.find('div', class_='lb-col lb-tiny-24 lb-mid-24')
                
                title_classes = {'lb-txt-bold', 'lb-txt-24', 'lb-h2', 'lb-title'}
                tags = div.find_all('h2')
                category_h2 = [tag for tag in tags if title_classes.issubset(set(tag.get('class', [])))][0]
                
                content = div.find('div', class_='lb-txt-16 lb-rtxt')
                
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                for a_tag in content.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))

                faqs = content.get_text().strip().split('Q:')[1:]
                for i, faq in enumerate(faqs):
                    que, ans = faq.split('?')[:2]
                    que = f'Q: {que.strip()}?'

                    output.append({
                    'question': que, 
                    'answer': ans.strip(),
                    'category':'Elastic Kubernetes',
                    'sub_category':category_h2.text.strip()})
                
                    progress_file.write(f'Scraped {i+1}/{len(faqs)} FAQs\n')
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')

            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped ElasticKubernetesFAQs\n')

# Amazon Lightsail FAQs (https://web.archive.org/web/20240727061427/https://aws.amazon.com/lightsail/faq/)
class LightsailFAQs():

    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727061427/https://aws.amazon.com/lightsail/faq/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/lightsail.csv'
        self.progress_file = f'{progress_directory}/lightsail.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                questions = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(questions):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text, 
                                'answer': content_div.get_text(), 
                                'category':'Lightsail',
                                'sub_category':category_h2.text})
                    
                    progress_file.write(f'Scraped {i+1}/{len(questions)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)            
            print('[DONE] Scraped LightsailFAQs\n')

# AWS Batch FAQs (http://web.archive.org/web/20240727090605/https://aws.amazon.com/batch/faqs/)
class BatchFAQs():

    def __init__(self) -> None:
        URL = 'http://web.archive.org/web/20240727090605/https://aws.amazon.com/batch/faqs/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/aws_batch.csv'
        self.progress_file = f'{progress_directory}/aws_batch.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                questions = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(questions):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text, 
                                'answer': content_div.get_text(),
                                'category':'Batch', 
                                'sub_category':category_h2.text})
                    
                    progress_file.write(f'Scraped {i+1}/{len(questions)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped BatchFAQs\n')            

# AWS Data Exchange FAQ:(http://web.archive.org/web/20240727090632/https://aws.amazon.com/data-exchange/faqs/)
class DataExchangeFAQs():

    def __init__(self) -> None:
        URL = 'http://web.archive.org/web/20240727090632/https://aws.amazon.com/data-exchange/faqs/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/data_exchange.csv'
        self.progress_file = f'{progress_directory}/data_exchange.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                try:
                    new_content = f"[{tag.text}]({tag['href']})"
                    return new_content
                except KeyError:
                    return str(tag)
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='lb-none-pad lb-none-v-margin lb-grid')
        output = []
        

        with open(self.progress_file, 'w') as progress_file:
            for section in sections:
                div = section.find('div', class_='lb-col lb-tiny-24 lb-mid-24')
                h2 = div.find('h2')
                progress_file.write(f'{"="*5} {f"{h2.text}" if h2 else ""} {"="*5}\n')
                
                content_divs = div.find_all('div', class_='lb-txt-16 lb-rtxt')
                for cd in content_divs:
                    for a_tag in cd.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))

                content = ''.join([div.get_text().strip() for div in content_divs])

                faqs = content.split('Q:')[1:]
                for i, faq in enumerate(faqs):
                    que, ans = faq.split('?')[:2]
                    que = f'Q: {que.strip()}?'

                    output.append({
                    'question': que, 
                    'answer': ans.strip(),
                    'category':'Data Exchange', 
                    'sub_category': h2.get_text().strip() if h2 else None})
                
                    progress_file.write(f'Scraped {i+1}/{len(faqs)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*((len(h2.get_text())+2) if h2 else 1)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False) 
            print('[DONE] Scraped DataExchangeFAQs\n')           

# AWS Elastic Beanstalk FAQ: (https://web.archive.org/web/20240727090637/https://aws.amazon.com/elasticbeanstalk/faqs/)
class ElasticBeanstalkFAQ():

    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727090637/https://aws.amazon.com/elasticbeanstalk/faqs/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/beanstalk.csv'
        self.progress_file = f'{progress_directory}/beanstalk.txt'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                try:
                    new_content = f"[{tag.text}]({tag['href']})"
                    return new_content
                except KeyError:
                    return str(tag)
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='lb-grid')
        output = []
        

        with open(self.progress_file, 'w') as progress_file:
            for section in sections:
                h2 = section.find('h2')
                progress_file.write(f'{"="*5} {f"{h2.text}" if h2 else ""} {"="*5}\n')
                
                faqs = section.find_all('div', class_='lb-txt-16 lb-rtxt')
                for i, faq in enumerate(faqs):
                    p_tags = faq.find_all('p')

                    for a_tag in p_tags[1].find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))

                    output.append({
                        'question': p_tags[0].get_text().strip(),
                        'answer': p_tags[1].get_text().strip(),
                        'category':'Elastic Beanstalk',
                        'sub_category': h2.get_text()
                    })
                    progress_file.write(f'Scraped {i+1}/{len(faqs)} FAQs\n')
                progress_file.write(f'{"="*5}{"="*((len(h2.get_text())+2) if h2 else 1)}{"="*5}\n\n')
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped ElasticBeanstalkFAQ\n')            

# AWS Fargate FAQs (https://web.archive.org/web/20240727090700/https://aws.amazon.com/fargate/faqs/)
class FragrateFAQs():
    
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727090700/https://aws.amazon.com/fargate/faqs/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/fragrate.csv'
        self.progress_file = f'{progress_directory}/fragrate.txt'

        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                questions = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(questions):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text, 
                                'answer': content_div.get_text(),
                                'category':'Fragrate', 
                                'sub_category':category_h2.text})
                    
                    progress_file.write(f'Scraped {i+1}/{len(questions)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped FragrateFAQs\n')            

# AWS Lambda FAQs (https://web.archive.org/web/20240727065740/https://aws.amazon.com/lambda/faqs/)
class LambdaFAQs():
    
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727065740/https://aws.amazon.com/lambda/faqs/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/lambda.csv'
        self.progress_file = f'{progress_directory}/lambda.txt'

        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                questions = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(questions):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text, 
                                'answer': content_div.get_text(),
                                'category':'Lambda',
                                'sub_category':category_h2.text})
                    
                    progress_file.write(f'Scraped {i+1}/{len(questions)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped LambdaFAQs\n')            

# AWS Outpost FAQs (https://web.archive.org/web/20240727090727/https://aws.amazon.com/outposts/rack/faqs/)
class OutpostFAQs():
    
    def __init__(self) -> None:
        URL = 'https://aws.amazon.com/outposts/rack/faqs/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/outpost.csv'
        self.progress_file = f'{progress_directory}/outpost.txt'

        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                questions = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(questions):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text, 
                                'answer': content_div.get_text(),
                                'category':'Outpost', 
                                'sub_category':category_h2.text})
                    
                    progress_file.write(f'Scraped {i+1}/{len(questions)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped OutpostFAQs\n')            

# Serverless Application Repository FAQs and Terms (https://web.archive.org/web/20240727090753/https://aws.amazon.com/serverless/serverlessrepo/faqs/)
class ServerlessApplicationRepositoryFAQs():
    
    def __init__(self) -> None:
        URL = 'https://web.archive.org/web/20240727090753/https://aws.amazon.com/serverless/serverlessrepo/faqs/'
        response = requests.get(URL,timeout=10)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.output_file = f'{csv_directory}/serverless_application_repository.csv'
        self.progress_file = f'{progress_directory}/serverless_application_repository.txt'

        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)

        if not os.path.exists(progress_directory):
            os.makedirs(progress_directory)

    def parse(self):
        def replace_a_tag(tag):
            '''Function to replace a tag with markdown format: (Text)[Link]'''
            if tag.name == 'a':
                new_content = f"[{tag.text}]({tag['href']})"
                return new_content
            return str(tag)
        
        # Extracting the sections
        sections = self.soup.find_all('div', class_='eb-groupable-faq-section-wrapper lb-grid')
        output = []
        total_questions = len([div for sec in sections for div in sec.find_all('div', class_='aws-rigel expandable-section')])

        with open(self.progress_file, 'w') as progress_file:
            progress_file.write(f'Total FAQs: {total_questions} | Total Categories: {len(sections)}\n\n')
            for section in sections:
                # Category of the FAQ
                category_h2 = section.find('h2', class_='section-expander-header-title')
                progress_file.write(f'{"="*5} {category_h2.text} {"="*5}\n')

                # Questions and Answer Expandable Divisions
                questions = section.find_all('div', class_='aws-rigel expandable-section')
                
                for i, div in enumerate(questions):
                    # Question
                    h3 = div.find('h3', class_='eb-header-title lb-txt-none lb-title')

                    # Answer
                    content_div = div.find('div', class_='eb-rich-text-content lb-rtxt')

                    # Replacing the html hyperlink with markdown hyperlink
                    for a_tag in content_div.find_all('a'):
                        a_tag.replace_with(replace_a_tag(a_tag))
                    
                    output.append({'question': h3.text, 
                                'answer': content_div.get_text(),
                                'category':'Serverless Application Repository', 
                                'sub_category':category_h2.text})
                    
                    progress_file.write(f'Scraped {i+1}/{len(questions)} FAQs\n')
                
                progress_file.write(f'{"="*5}{"="*(len(category_h2.text)+2)}{"="*5}\n\n')
                    
            df = pd.DataFrame(output)
            df.to_csv(self.output_file, index=False)
            print('[DONE] Scraped ServerlessApplicationRepositoryFAQs\n')            


if __name__ == '__main__':
    print("Scrapping Started...")

    AutoScalingFAQs().parse()
    ElasticContainerRegistryFAQs().parse()
    ElasticContainerServiceFAQs().parse()
    EC2FAQs().parse()
    ElasticKubernetesFAQs().parse()
    LightsailFAQs().parse()
    BatchFAQs().parse()
    DataExchangeFAQs().parse()
    ElasticBeanstalkFAQ().parse()
    FragrateFAQs().parse()
    LambdaFAQs().parse()
    OutpostFAQs().parse()
    ServerlessApplicationRepositoryFAQs().parse()

    print("Scrapping Ended...")