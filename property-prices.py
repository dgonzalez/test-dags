from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

with DAG(
    'property-prices',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description='Some calculations around property prices',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['property'],
) as dag:

    t1 = DummyOperator(
        task_id='init'
    )

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t2 = BashOperator(
        task_id='task_2',
        bash_command='date',
    )

    k = KubernetesPodOperator(
	name="hello-dry-run",
	image="debian",
	cmds=["bash", "-cx"],
	arguments=["echo", "10"],
        namespace="default"
	labels={"foo": "bar"},
	task_id="dry_run_demo",
	do_xcom_push=True,
    )

    t1 >> t2 >> k
