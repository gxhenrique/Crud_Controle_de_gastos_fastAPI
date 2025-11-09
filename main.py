from fastapi import FastAPI,Depends,HTTPException,status

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.financas import Categoria
from models.financas import Transacoes

from conf.db_session import create_session

from schemas.schema import SchemaCategoria
from schemas.schema import SchemaTransacoes

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


def get_db():
    db = create_session()
    try:
        yield db
    finally:
        db.close()


@app.get('/financa')
def root_teste(db: Session = Depends(get_db)):

    categoria = db.query(Categoria).all()
    transacoes = db.query(Transacoes).all()

    return transacoes,categoria


@app.post('/financa/gastos')
def post_gatos(cate: SchemaCategoria, tran: SchemaTransacoes, db: Session = Depends(get_db) ):

    nova_categoria: Categoria = Categoria(
        nome = cate.nome,
        descricao = cate.descricao
    )

    nova_transacao : Transacoes = Transacoes(
        tipo = tran.tipo,
        valor = tran.valor,
        descricao = tran.descricao,
        data = tran.data,
        categoria=nova_categoria

    )

    db.add(nova_categoria)
    db.add(nova_transacao)
    db.commit()

    db.refresh(nova_transacao)
    db.refresh(nova_categoria)

    return {
        'Categoria': f'{nova_categoria}', 
        'transações': f'{nova_transacao}'
        }



@app.put('/financa/atualizar/{id_categoria}/{id_transacao}')
def put_categoria_trasacoes(
    id_categoria:int , 
    id_transacao:int,
    nova_categaria: SchemaCategoria, 
    nova_transacao: SchemaTransacoes, 
    db: Session = Depends(get_db)):

    categoria = db.query(Categoria).filter(Categoria.id == id_categoria).first()
    transacoes = db.query(Transacoes).filter(Transacoes.id == id_transacao).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria com o id {categoria.id} não encontrado'
        )
    
    if not transacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria com o id {transacoes.id} não encontrado'
        )
   
   

    categoria.nome = nova_categaria.nome
    categoria.descricao = nova_categaria.descricao
   
    transacoes.tipo = nova_transacao.tipo
    transacoes.valor = nova_transacao.valor
    transacoes.descricao = nova_transacao.descricao
    transacoes.data = nova_transacao.data

    db.commit()
    db.refresh(transacoes)
    db.refresh(categoria)
   
   
    
    return {
        'Mensagem': 'Categoria e transação atualizado com sucesso',
        'Categoria': f'{categoria}',
        'Transação': f'{transacoes}'
    }


@app.delete('/financa/delete/{id_categoria}/{id_transacao}')
def delete_categoria_transacoes(
    id_categoria: int,
    db: Session = Depends(get_db)):


    categoria = db.query(Categoria).filter(Categoria.id == id_categoria).first()
    transacoes = db.query(Transacoes).filter(Transacoes.id == id_categoria).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Categoria não encontrado'
        )
    if not transacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='transação não encontrado'
        )
    
    try:
        db.delete(categoria)
        db.delete(transacoes)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Erro ao tenta apagar o elemento {e}'
        )


    return {'Mensagem': f'Categoria {categoria.id} deletada com sucesso'}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://127.0.0.1:5500"] se usar o Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

