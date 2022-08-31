from threading import Thread, Semaphore
import random
import time


class DiningPhilosophers:
    # constructor
    def __init__(self, number_of_philosophers=5, meal_size=7):
        """
        meal_size: jobs
        philosophers: processos
        chopsticks: resources (como se fosse garfo e faca, o filósofo só pode comer se ele estiver com ambos)
        meal_size = 7 & number_of_philosophers = 5 -> [7, 7, 7, 7, 7], então, cada filósofo tem 7 "trabalhos" para fazer
        """

        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.status = ["  P  " for _ in range(number_of_philosophers)]
        self.chopstick_holders = ["     " for _ in range(number_of_philosophers)]

    def philosopher(self, i):
        j = (i + 1) % 5
        """
            
            j será usado para representar o último filósofo da lista, por exemplo,
            se tivermos cinco filósofos [0, 1, 2, 3, 4, 5], o último não terá um segundo
            talher, então, usando (i+1) % 5 a lista ficará assim: [0, 1, 2, 3, 4, 0] (lembre-se que estamos em uma mesa redonda,
            então o último elemento tem que ser relacionado ao primeiro elemento)
        """

        #  esse loop só terminará quando cada filósofo terminar sua refeição
        while self.meals[i] > 0:
            self.status[i] = "  P  "  # todos eles irão começar pensando
            time.sleep(random.random())  # aplicar um sleep entre 0 e 1 no filósofo
            self.status[i] = "  _  "
            if self.chopsticks[i].acquire(
                timeout=1
            ):  # checar se o talher está sendo utilizado
                self.chopstick_holders[
                    i
                ] = " /   "  # se o talher não está sendo usuado, atribua-o para o filósofo
                time.sleep(
                    random.random()
                )  # depois de atribuir o talher, aplica-se o sleep no filósofo
                if self.chopsticks[j].acquire(
                    timeout=1
                ):  # aqui checaremos se o próximo talher está sendo utilizado ou não
                    self.chopstick_holders[
                        i
                    ] = " / \\ "  # se ele não estiver sendo utilizado, atribua-o para o filósofo
                    self.status[
                        i
                    ] = "  C  "  # então atribuiremos o status de: C (comendo) para o filósofo
                    time.sleep(random.random())  # aplicar um sleep entre 0 e 1 no filósofo
                    self.meals[
                        i
                    ] -= 1  # subtrair uma meal do filósofo 
                    self.chopsticks[
                        j
                    ].release()  # depois de comer, liberar o segundo talher
                    self.chopstick_holders[
                        i
                    ] = " /   "  # atribuir novamente apenas um talher para o filósofo
                self.chopsticks[i].release()  # liberar o primeiro talher
                self.chopstick_holders[
                    i
                ] = "     "  # depois de fazer uma refeição, atribuir nenhum talher ao filósofo
                self.status[i] = "  P  "  # O status voltará a ser pensando


def main():
    n = 5  # definir numero de filósofos
    m = 7  # definir o tamanho da refeição de cada filósofo

    dining_philosophers = DiningPhilosophers(n, m)  # instanciando a classe
    philosophers = [
        Thread(target=dining_philosophers.philosopher, args=(i,)) for i in range(n)
    ]  # inicializando a thread
    for philosopher in philosophers:  # irá percorrer por todos os filósofos
        philosopher.start()  # começar a thread
    while ( sum(dining_philosophers.meals) > 0):  # checar se ainda há refeições para serem consumidas
        print("=" * (n * 5))  # printar a quantidade de refeições
        print(
            "".join(map(str, dining_philosophers.status)),
            " : ",
            str(dining_philosophers.status.count("  C  ")),
        )  # printar o status em que o filósofo se encontra
        print("".join(map(str, dining_philosophers.chopstick_holders)))
        print(
            "".join("{:3d}  ".format(m) for m in dining_philosophers.meals),
            " : ",
            str(sum(dining_philosophers.meals)),
        )  # printar a quantidade de refeições de cada filósofo
        time.sleep(0.1)  # um sleep antes de ir para o próximo step

    for philosopher in philosophers:
        philosopher.join()  # verifica se não há pararelismo durante a execução da thread


if __name__ == "__main__":
    main()  # executa a função
