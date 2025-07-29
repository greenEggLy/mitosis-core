import json
import time

import random

def random_string(length) -> str:
	characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	return ''.join(random.choice(characters) for _ in range(length))

def CreatePost(max_posts, max_users, post_length) -> dict:
	print(max_posts)
	initial_post = {}
	user_post = {}
	for i in range(max_posts):
		timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
		post_id = f"{timestamp}-{i}"

		content = random_string(post_length)
		initial_post[post_id] = {"timestamp": timestamp, 'content': content}

		username = f"username_{random.randint(1, max_users-1)}"
		if username not in user_post.keys():
			user_post[username] = []
		user_post[username].append(post_id)
	
	return initial_post, user_post

def CreateUser(max_users, max_followers) -> dict:
	user_info = {}
	for i in range(max_users):
		username = f"username_{i}"
		password = f"pwd_{i}"
		followers = random.randint(1, max_followers)
		followers = [f"username_{random.randint(1, max_users)}" for _ in range(followers)]
		user_info[username] = {'password': password, 'followers': followers, 'posts': []}
	
	return user_info

def get_input():
    return {
		"output": {},
		'max_users': 10000,
        'max_followers': 500,
        'max_posts': 5000,
        'post_length': 20,
	}

def lambda_handler(params):
	with open("./haha.txt", 'w') as f:
		f.write("haha\n")
	start_time = time.time()
	oa = params['output']
	max_users = params['max_users']  # 1000000
	max_followers = params['max_followers']
	max_posts = params['max_posts']
	post_length = params['post_length']
	start_compute_time = time.time()
	user_info = CreateUser(max_users, max_followers)
	initial_post, user_post = CreatePost(max_posts, max_users, post_length)
	for username in user_post.keys():
		user_info[username]['posts'].extend(user_post[username])
	com_data = {'user_info': user_info, 'post_info': initial_post}

	end_compute_time = time.time()
	start_output_time = time.time()
	# md.output(['stage2'], f'{oa}-2', com_data)
	# md.output(['stage3'], f'{oa}-3', com_data)
	# md.output(['stage4'], f'{oa}-4', com_data)
	# md.output(['stage5'], f'{oa}-5', com_data)

	end_output_time = time.time()
	end_time = time.time()

	return_val = {
		'process_time': end_time - start_time,
		'input_time': 0,
		'compute_time': end_compute_time - start_compute_time,
		'output_time': end_output_time - start_output_time,
	}
	
	return {
		'statusCode': 200,
		'body': json.dumps(return_val)
	}
 
