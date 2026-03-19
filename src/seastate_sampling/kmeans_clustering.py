import numpy as np

def distance(p1,p2):
    return np.sqrt(np.sum((p1-p2)**2))

def assign_clusters(X, clusters, k):
    for i in range(k):
        clusters[i]['points'] = []
    for idx in range(X.shape[0]):
        dist = []
        
        curr_x = X[idx]
        
        for i in range(k):
            dis = distance(curr_x,clusters[i]['center'])
            dist.append(dis)
        curr_cluster = np.argmin(dist)
        clusters[curr_cluster]['points'].append(curr_x)
    return clusters

def update_clusters(X, clusters, k):
    for i in range(k):
        points = np.array(clusters[i]['points'])
        if points.shape[0] > 0:
            clusters[i]['center'] = points.mean(axis=0)
        else:
            # reinitialize to a random point from data
            clusters[i]['center'] = X[np.random.randint(0, X.shape[0])]
        
    return clusters


def pred_cluster(X, clusters, k):
    pred = []
    for i in range(X.shape[0]):
        dist = []
        for j in range(k):
            dist.append(distance(X[i],clusters[j]['center']))
        pred.append(np.argmin(dist))
    return pred

def build_clusters(X,k,iterations):
    clusters = {}
    x_min, x_max = X[:,0].min(), X[:,0].max()
    y_min, y_max = X[:,1].min(), X[:,1].max()
    X_scaled = np.zeros_like(X)
    X_scaled[:,0] = (X[:,0] - X[:,0].min()) / (X[:,0].max() - X[:,0].min())  # Te
    X_scaled[:,1] = (X[:,1] - X[:,1].min()) / (X[:,1].max() - X[:,1].min())  # Hm0
    for idx in range(k):
        center = (np.random.uniform(0,1), np.random.uniform(0,1))
        cluster = {
            'center' : center,
            'points' : []
        }

        clusters[idx] = cluster
    
    for _ in range(iterations):
        print(f'\rIteration {_+1}/{iterations}...', end='', flush=True)
        clusters = assign_clusters(X_scaled, clusters, k)
        clusters = update_clusters(X_scaled, clusters, k)

    pred = pred_cluster(X_scaled, clusters, k)

    for idx in clusters:
        c = clusters[idx]['center']
        unscaled = np.array([
            c[0] * (x_max - x_min) + x_min,
            c[1] * (y_max - y_min) + y_min
        ])
        clusters[idx]['center'] = unscaled

    return clusters, pred