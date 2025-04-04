## How-to Guide
### 1. Install prerequisites
- python 3.10
```shell
pip install -r requirements.txt
```

### 2. Create your secret file
After creating, please replace mine at `secrets/mle-course-00d1417f42ca.json`



Use: `ansible -i inventory all -m ping`
**Note:** Update `state: absent` to destroy the instance

### 3. Provision the server and firewall rule
    ```shell
    cd playbooks
    ansible-playbook create_compute_instance.yaml
    ```

#### 4. Install Docker and run the application
After your instance has been started as the folowing image, get the External IP (e.g., `104.198.109.131` as in the example) and replace it in the inventory file

![Compute Engine](./imgs/compute_engine.png)
, and run the following commands:
    
    ```shell
    cd playbooks
    ansible-playbook -i ../inventory deploy_jelkins.yml
    ```
, now, you should be able to access your application via `http://104.198.109.131:30000/docs`